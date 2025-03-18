import time
import uuid
import random

from locust import task, FastHttpUser, events, constant_pacing
from sqlalchemy.orm import Session

from mock_generator import MockSensorDataGenerator
from db import models
from db.models import Base
from db.database import engine, get_db

from configurations import SEGMENT_SIZE

# Global database session (initialized when the test starts)
session: Session = None


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Event listener that runs when the Locust test starts.

    - Initializes the database session.
    - Ensures all database tables are created.
    """
    global session
    Base.metadata.create_all(engine) # Create tables if they don't exist
    session = get_db() # Initialize the database session
    print("test start!")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Event listener that runs when the Locust test stops.

    - Commits and closes the database session.
    """
    global session
    session.commit() # Commit any remaining transactions
    session.close() # Close the session
    print("test stop!")


class SpringLocust(FastHttpUser):
    """Locust user simulating sensor data transmission to a server.

    - Sends mock sensor data at fixed intervals.
    - Records latency timestamps in the database.
    """
    client = None # HTTP client used to send requests

    # Ensures the task runs (at most) once every SEGMENT_SIZE seconds
    wait_time = constant_pacing(SEGMENT_SIZE / 1000) # Convert ms to seconds

    def __init__(self, *args, **kwargs):
        """Initialize the Locust user instance."""
        super().__init__(*args, **kwargs)
        self.user_id = None
        self.generator = None

    def on_start(self):
        """Called when a new Locust user starts.

        - Generates a unique user ID.
        - Initializes a mock sensor data generator.
        """
        self.user_id = str(uuid.uuid4()) # Assign a unique user ID via UUID
        self.generator = MockSensorDataGenerator(self.user_id) # Initialize mock data generator
        return super().on_start()

    @task
    def send_data(self):
        """Simulates sending sensor data to the server.

        - Generates mock sensor data.
        - Sends data to the server via an HTTP POST request.
        - Logs request timestamps in the database.
        """
        global session
        if (self.generator is not None):
            msg = self.generator.generate_data() # Generate mock sensor data
            # Send sensordata to producer
            self.client.post("/", json=msg)
            # Record the timestamps for latency calculation
            data = models.StartRecord(
                connection_id=msg["connection_id"],
                timestamp=msg["timestamp"],
                response_time=int(time.time()*1000) # Convert seconds to milliseconds
            )
            session.add(data) # Add record to the database
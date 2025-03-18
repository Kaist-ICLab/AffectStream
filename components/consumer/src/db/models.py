from sqlalchemy import Column, String, BigInteger, Double, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# Define the base class for all models
Base = declarative_base()


class EndRecord(Base):
    """Represents a record for tracking when a process ends."""

    __tablename__ = "end_record" # Database table name

    id = Column(
        BigInteger,
        primary_key=True
    )
    connection_id = Column(
        String(255),
        nullable=False,
    )
    timestamp = Column(
        BigInteger,
        nullable=False,
    )
    inference_time = Column(
        BigInteger,
        nullable=False,
    )

    def __repr__(self) -> str:
        """String representation of the EndRecord object."""
        return f"ConsumerRecord(id={self.id}, consume_time={self.timestamp}, inference_time={self.inference_time})"


class User(Base):
    """Represents a user entity in the system."""

    __tablename__ = "users" # Database table name

    id = Column(
        BigInteger,
        primary_key=True
    )
    age = Column(
        BigInteger,
        nullable=False,
    )
    gender = Column(
        String(255),
        nullable=False,
    )

    def __repr__(self) -> str:
        """String representation of the User object."""
        return f"User(id={self.id}, age={self.age}, gender={self.gender})"


class SensorChest(Base):
    """Represents chest sensor data collected from a user."""

    __tablename__ = "sensor_chests" # Database table name

    id = Column(
        BigInteger,
        primary_key=True
    )
    user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
    )
    ecg = Column(
        Double,
        nullable=False,
    )

    def __repr__(self) -> str:
        """String representation of the SensorChest object."""
        return f"SensorChest(user_id={self.user_id})"

import time
import uuid
from typing import Tuple, List, Optional

from schema import ChestDeviceSensorRecord, Axis, ChestDeviceSensorValue
from configurations import SEGMENT_SIZE, SAMPLING_RATE

class MockSensorDataGenerator:
    """Generates mock sensor data for chest device recordings."""

    file_data: List[Tuple[int, int, int, int, int, int, int, int]] = []

    def __init__(self, user_id):
        """Initialize the sensor data generator.
        
        Args:
            user_id (str): Unique identifier for the user.
        """
        self.user_id = user_id
        self.counter: int = 0

        # Load the data file only once for efficiency
        if not MockSensorDataGenerator.file_data:
            MockSensorDataGenerator.file_data = self.preprocess_file(None)

    @staticmethod
    def preprocess_file(filename: Optional[str]) -> List[Tuple[int, int, int, int, int, int, int, int]]:
        """Preprocesses the input file to load sensor data.
        
        Args:
            filename (Optional[str]): Path to the file containing sensor data.
        
        Returns:
            List of tuples containing sensor data.
        """
        if filename is None:
            filename = "../data/respiban.tsv"

        with open(filename) as f:
            result = []
            data = [tuple(map(int, line.split("\t"))) for line in f]

            # Extend the dataset to match the required segment size
            required_length = (int) (SEGMENT_SIZE * SAMPLING_RATE / 1000)
            while len(result) < required_length:
                result.extend(data)
            return result

    def generate_data(self) -> ChestDeviceSensorRecord:
        """Generates mock sensor data for a predefined segment size.

        Returns:
            ChestDeviceSensorRecord: A dictionary containing generated sensor data.
        """
        num_idx = (int) (SEGMENT_SIZE * SAMPLING_RATE / 1000)
        segment_data = MockSensorDataGenerator.file_data[0 : num_idx]

        # Extract sensor values from tuples
        chest_ecg = [ecg for ecg, _, _, _, _, _, _, _ in segment_data]
        chest_eda = [eda for _, eda, _, _, _, _, _, _ in segment_data]
        chest_emg = [emg for _, _, emg, _, _, _, _, _ in segment_data]
        chest_temp = [temp for _, _, _, temp, _, _, _, _ in segment_data]
        chest_acc = [{"x": x, "y": y, "z": z} for _, _, _, _, x, y, z, _ in segment_data]
        chest_resp = [resp for _, _, _, _, _, _, _, resp in segment_data]

        # Construct the final sensor data record
        return {
            "user_id": self.user_id,
            "connection_id": str(uuid.uuid4()),
            "timestamp": int(time.time() * 1000),
            "segment_size": SEGMENT_SIZE,
            "value": {
                "chest_acc": {"hz": SAMPLING_RATE, "value": chest_acc},
                "chest_ecg": {"hz": SAMPLING_RATE, "value": chest_ecg},
                "chest_eda": {"hz": SAMPLING_RATE, "value": chest_eda},
                "chest_emg": {"hz": SAMPLING_RATE, "value": chest_emg},
                "chest_temp": {"hz": SAMPLING_RATE, "value": chest_temp},
                "chest_resp": {"hz": SAMPLING_RATE, "value": chest_resp}
            }
        }

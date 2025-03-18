from typing import TypedDict, List

'''''
    The example of data following this schema:
    {
        "user_id": 1,
        "connection_id": 1020122,
        "timestamp": 12312412312,
        "segment_size": 1000,
        "value": {
            "chest_acc": {
            "hz": 700,
            "value": []
            },
            "chest_ecg": {
            "hz": 700,
            "value": []
            },
            "chest_eda": {
            "hz": 700,
            "value": []
            },
            "chest_emg": {
            "hz": 700,
            "value": []
            },
            "chest_temp": {
            "hz": 700,
            "value": []
            },
            "chest_resp": {
            "hz": 700,
            "value": []
            }
        }
    }
'''''

# Represents a single 3D axis measurement (e.g., accelerometer data)
class Axis(TypedDict):
    x: int
    y: int
    z: int


# Chest Accelerometer
class ChestACC(TypedDict):
    hz: int
    value: List[Axis]


# Chest Electrocardiogram
class ChestEGC(TypedDict):
    hz: int
    value: List[int]


# Chest Electrodemal
class ChestEDA(TypedDict):
    hz: int
    value: List[int]


# Chest Electromyogram
class ChestEMG(TypedDict):
    hz: int
    value: List[int]


# Chest Temperature
class ChestTemp(TypedDict):
    hz: int
    value: List[int]


# Chest Respiration
class ChestResp(TypedDict):
    hz: int
    value: List[int]

# Represents all chest device sensor values
class ChestDeviceSensorValue(TypedDict):
    chest_acc: ChestACC
    chest_ecg: ChestEGC
    chest_eda: ChestEDA
    chest_emg: ChestEMG
    chest_temp: ChestTemp
    chest_resp: ChestResp

# Represents a single chest device sensor record
class ChestDeviceSensorRecord(TypedDict):
    user_id: str
    connection_id: str
    timestamp: int
    segment_size: int
    value: ChestDeviceSensorValue

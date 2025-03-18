from typing import TypedDict, List
class Axis(TypedDict):
    x: float
    y: float
    z: float


# Chest Accelerometer
class ChestACC(TypedDict):
    hz: int
    value: List[Axis]


# Chest Electrocardiogram
class ChestEGC(TypedDict):
    hz: int
    value: List[float]


# Chest Electrodemal
class ChestEDA(TypedDict):
    hz: int
    value: List[float]


# Chest Electromyogram
class ChestEMG(TypedDict):
    hz: int
    value: List[float]


# Chest Temperature
class ChestTemp(TypedDict):
    hz: int
    value: List[float]


# Chest Respiration
class ChestResp(TypedDict):
    hz: int
    value: List[float]

# Wrist
class WristACC(TypedDict):
    hz: int
    value: List[Axis]

class WristBVP(TypedDict):
    hz: int
    value: List[float]

class WristEDA(TypedDict):
    hz: int
    value: List[float]

class WristTemp(TypedDict):
    hz: int
    value: List[float]

class DeviceSensorValue(TypedDict):
    chest_acc: ChestACC
    chest_ecg: ChestEGC
    chest_eda: ChestEDA
    chest_emg: ChestEMG
    chest_temp: ChestTemp
    chest_resp: ChestResp

class SensorValue(TypedDict):
    user_id: str
    connection_id: str
    timestamp: int
    segment_size: int
    value: DeviceSensorValue

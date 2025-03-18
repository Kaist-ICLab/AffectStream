"""
main consumer code.
"""
import math
import time
from typing import List
import pandas as pd
import numpy as np
import os

from aiokafka import AIOKafkaConsumer
from aiokafka.helpers import create_ssl_context

from cache.table import Cache, get_context_cache
from configurations import InferenceConfigurations, KafkaConfigurations
from db.database import get_context_db
from db.models import EndRecord
from logger.ConsumerLogger import ConsumerLogger
from schema.chest import DeviceSensorValue, SensorValue
from serde.deserializer import KafkaDeserializer
import signal
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = ConsumerLogger() # Initialize logger

# Initialize Kafka deserializer for incoming messages
deserializer = KafkaDeserializer(
    topic=KafkaConfigurations.topic
)

# Thread pool executor for parallel execution
thread_pool = ThreadPoolExecutor(max_workers=5)

async def process_data(sensor_data: SensorValue, cache: Cache, db):
    """
    Process each sensor message from Kafka.

    Args:
        sensor_data (SensorValue): Deserialized sensor data from Kafka.
        cache (Cache): In-memory storage for sensor data.
        db: SQLAlchemy session object for storing timestamps.

    - Extracts features from sensor data.
    - Stores processed data in a global Pandas dataframe.
    - Logs latency and saves the timestamp in the database.
    """

    # Record the start time for inference (benchmarking)
    start_time = int(time.time() * 1000)
    user_id = sensor_data['user_id']
    # Initialize user cache if not already present
    if cache.get(user_id) is None:
        cache[user_id] = {}

    # Check for missing values in sensor data
    has_missing_value = sanity_check_no_missing(sensor_data)
    if not has_missing_value:
        cache[user_id] = extend_data(cache[user_id], sensor_data["value"])

    while is_valid_length(cache[user_id], InferenceConfigurations.window_size):
        # feature extraction
        new_feat = feature_extract_sensor(user_id, sensor_data["timestamp"], cache[user_id])

        # load model & inference
        model = models[user_id]
        if model is None:
            model = model_load()
            models[user_id] = model
        pred, xai = model_adapt_and_predict(model, sensor_features=new_feat[new_feat.columns.difference(['user_id', 'timestamp'])])
        logger.info("Prediction for user, %s is: %s", user_id, bool(pred))

        # Remove oldest data from cache if overlap condition is met
        if is_valid_length(cache[user_id], InferenceConfigurations.overlap_size):
            window = cache[user_id]
            cache[user_id] = remove_overlap(window)

    logger.info(f"[Success]: user_id: {user_id}, created_at: {sensor_data['timestamp']}, latency: {start_time - sensor_data['timestamp']}")

    # log timestamp to database
    end_record = EndRecord(
        connection_id=sensor_data['connection_id'],
        timestamp=start_time,
        inference_time=int(time.time() * 1000),
    )
    db.add(end_record)

async def on_signal_exit(loop, consumer):
    """
    Gracefully handles consumer termination.

    - Stops Kafka consumer.
    - Commits remaining processed data to the database.
    - Logs final extracted features.
    """
    await consumer.stop()

    db.commit()
    logger.info("Wrote timestamps into DB, ready to shutdown")

    loop.stop()

async def main():
    """
    Main function to start Kafka consumer.

    - Connects to Kafka and listens for messages.
    - Deserializes incoming messages and processes sensor data.
    - Stores inference timestamps in the database before termination.
    """
    consumer = AIOKafkaConsumer(
        KafkaConfigurations.topic,
        bootstrap_servers=KafkaConfigurations.kafka_host,
        ssl_context=create_ssl_context(),
        security_protocol="SASL_SSL",
        sasl_mechanism="SCRAM-SHA-512",
        sasl_plain_username=KafkaConfigurations.sasl_user,
        sasl_plain_password=KafkaConfigurations.sasl_password,
        group_id=KafkaConfigurations.consumer_group_id,
        auto_offset_reset="earliest", # Start from the beginning if no offset is found 
        value_deserializer=deserializer.deserialize,
        check_crcs=False,
        max_partition_fetch_bytes=KafkaConfigurations.consumer_max_fetch_size,
        max_poll_records=100
    )

    # Register termination signal handler
    loop.add_signal_handler(signal.SIGTERM, lambda l, c: l.create_task(on_signal_exit(l, c)), loop, consumer)

    # Start Kafka consumer
    await consumer.start()
    logger.info("Kafka consumer started!")

    try:
        async for msg in consumer:
            logger.info(f"Received message: topic: {msg.topic}, partition: {msg.partition}, offset: {msg.offset}, key: {msg.key}")
            data: SensorValue = msg.value
            await process_data(data, cache, db)

    finally:
        await consumer.stop()
        db.commit()
        logger.info("Wrote timestamps into DB, ready to shutdown")


def sanity_check_no_missing(record: SensorValue):
    """Checks for missing values in sensor data."""
    sensor_value = record["value"]
    segment_size = record["segment_size"]
    columns = vars(DeviceSensorValue).get("__annotations__").keys()
    for col in columns:
        if col in ['label', 'domain']:
            continue
        value_list: List = sensor_value[col]["value"]
        sampling_rate: int = sensor_value[col]["hz"]
        num_idx: int = (int) (sampling_rate * segment_size / 1000)
        sanity_check_list = []
        if col in ["chest_acc", "wrist_acc"]:
            for i in range(num_idx):
                x = value_list[i]["x"]
                y = value_list[i]["y"]
                z = value_list[i]["z"]
                sanity_check_list += [x, y, z]
        else:
            sanity_check_list = value_list

        if any(math.isnan(a) for a in sanity_check_list):
            print(f'modality : {col} has NAN value, so pass')
            return True
    return False

def sanity_check_in_order(record_list: List[SensorValue]):
    """Checks for orders of values in sensor data."""
    timestamp_list = []

    for record in record_list:
        timestamp_list.append(record['timestamp'])

    is_in_order = all(timestamp_list[i] <= timestamp_list[i + 1] for i in range(len(timestamp_list) - 1))

    if is_in_order:
        return 1
    else:
        return 0

def extend_data(sensor_data, new_data: DeviceSensorValue) -> DeviceSensorValue:
    """
    Extend the window with new data.
    :param sensor_data: a list of sensor data.
    :param new_data: a list of new sensor data.
    :return: a list of sensor data extended with new data.
    """
    if not sensor_data:
        # The cache is empty
        return new_data
    data: DeviceSensorValue = sensor_data
    columns = vars(DeviceSensorValue).get("__annotations__").keys()
    for col in columns:
        if col in ['label', 'domain']:
            continue
        data[col]["value"].extend(new_data[col]["value"])
    return data
    
def remove_overlap(sensor_data: DeviceSensorValue) -> DeviceSensorValue:
    """
    Remove the overlap data from the window.
    :param sensor_data: a list of sensor data.
    :param overlap_size: the size of the overlap.
    :return: a list of sensor data without overlap.
    """
    columns = vars(DeviceSensorValue).get("__annotations__").keys()
    for col in columns:
        if col in ['label', 'domain']:
            continue
        sampling_rate = sensor_data[col]["hz"]
        sensor_data[col]["value"] = sensor_data[col]["value"][InferenceConfigurations.overlap_size * sampling_rate:]
    return sensor_data
    
def is_valid_length(sensor_data: DeviceSensorValue, length) -> bool:
    """
    Check if the window has enough data to be used for inference.
    :return: True if the window has enough data, False otherwise.
    """
    columns = vars(DeviceSensorValue).get("__annotations__").keys()
    for col in columns:
        if col in ['label', 'domain']:
            continue
        sampling_rate = sensor_data[col]["hz"]
        if len(sensor_data[col]["value"]) < length * sampling_rate:
            return False
    return True

def feature_extract_sensor(user_id: str, timestamp: int, sensor_data: DeviceSensorValue) -> pd.DataFrame:
    feature_dict = {
        "user_id": user_id,
        "timestamp": timestamp
    }

    columns = vars(DeviceSensorValue).get("__annotations__").keys()
    for col in columns:
        if col in ['label', 'domain']:
            continue
        values = []
        sampling_rate = sensor_data[col]["hz"]
        window_length = InferenceConfigurations.window_size * sampling_rate
        if col in ["chest_acc", "wrist_acc"]:  # l2-norm of X, Y, Z axis
            acc_list = sensor_data[col]["value"]
            for acc_i in range(window_length):
                acc_x = acc_list[acc_i]["x"]
                acc_y = acc_list[acc_i]["y"]
                acc_z = acc_list[acc_i]["z"]
                values.append(np.sqrt(np.power(acc_x, 2) + np.power(acc_y, 2) + np.power(acc_z, 2)))
        else:
            values.extend(sensor_data[col]["value"][:window_length])

        feature_dict[f"{col}_mean"] = np.mean(values)
        feature_dict[f'{col}_std'] = np.std(values)
        feature_dict[f"{col}_max"] = np.max(values)
        feature_dict[f'{col}_min'] = np.min(values)

    _feature_df = pd.DataFrame([feature_dict])

    return _feature_df

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    with get_context_cache() as cache, get_context_db() as db:
        logger.info("DB connected!")
        logger.info(KafkaConfigurations())
        loop.run_until_complete(main())
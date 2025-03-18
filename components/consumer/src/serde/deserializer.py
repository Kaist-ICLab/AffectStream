"""
Adapter for aiokafka consumer.
For the implementation idea, refer to 
https://github.com/DisasterAWARE/aws-glue-schema-registry-python/blob/main/src/aws_schema_registry/adapter/kafka.py.
"""
from aws_schema_registry import SchemaRegistryClient, KafkaDeserializer as _KafkaDeserializer
import boto3
from configurations import KafkaConfigurations

class KafkaDeserializer:
    """
    Adapter for aiokafka consumer.
    """

    def __init__(self, topic: str):
        # Create a aws session from the IAM account credentials.
        aws_session = boto3.Session(
            aws_access_key_id=KafkaConfigurations.iam_access_key_id,
            aws_secret_access_key=KafkaConfigurations.iam_secret_access_key,
            region_name=KafkaConfigurations.aws_region_name,
        )
        glue_client = aws_session.client("glue")

        # Create the schema registry client and the deserializer that depends upon it.
        schema_registy_client = SchemaRegistryClient(
            glue_client,
            registry_name=KafkaConfigurations.registry_name
        )
        self._deserializer = _KafkaDeserializer(client=schema_registy_client)
        self.topic = topic

    def deserialize(self, bytes_):
        """
        deserializer function to use as a "value_deserializer" argument
         of AIOKafkaConsumer constructor.
        """
        return self._deserializer.deserialize(self.topic, bytes_).data

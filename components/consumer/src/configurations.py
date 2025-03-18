import os
import uuid


class DBConfigurations:
    """Database configurations for PostgreSQL.

    - Retrieves environment variables for database connection.
    - Defaults to localhost and standard PostgreSQL settings if environment variables are not provided.
    """
    # Database connection settings
    postgres_host = str(os.getenv("POSTGRES_HOST") or "localhost")
    postgres_port = int(os.getenv("POSTGRES_PORT") or "5432")
    postgres_db =  str(os.getenv("POSTGRES_DB") or "postgres")
    postgres_username = str(os.getenv("POSTGRES_USER") or "postgres")
    postgres_password = str(os.getenv("POSTGRES_PASSWORD") or "postgres")

    # SQLAlchemy connection URL
    sql_alchemy_url = (
        f"postgresql://{postgres_username}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
    )


class KafkaConfigurations:
    """Kafka configurations for message processing.

    - Retrieves Kafka connection credentials and topic settings from environment variables.
    - Uses IAM authentication details if required.
    """
    # Connection options
    kafka_host = str(os.getenv("KAFKA_HOST") or "")
    sasl_user = str(os.getenv("SASL_USERNAME") or "")
    sasl_password = str(os.getenv("SASL_PASSWORD") or "")
    iam_access_key_id = str(os.getenv("IAM_ACCESS_KEY_ID") or "")
    iam_secret_access_key = str(os.getenv("IAM_SECRET_ACCESS_KEY") or "")
    aws_region_name = str(os.getenv("AWS_REGION_NAME") or "")
    registry_name = str(os.getenv("REGISTRY_NAME") or "")

    # Consumer options
    topic = str(os.getenv("TOPIC") or "chest") # Kafka topic to subscribe to
    partitions = int(os.getenv("PARTITIONS") or "6") # Number of partitions
    consumer_max_fetch_size = int(os.getenv("CONSUMER_MAX_FETCH_SIZE") or "10485760") # Max fetch size per partition (10MB)
    consumer_group_id = str(os.getenv("CONSUMER_GROUP_ID") or uuid.uuid4()) # Unique consumer group ID
    consumer_instance_id = str(os.getenv("CONSUMER_INSTANCE_ID") or uuid.uuid4()) # Unique instance ID for consumer

    def __str__(self):
        """Returns a string representation of Kafka configuration details."""
        return f"kafka host: {self.kafka_host}, topic: {self.topic}, consumer_group_id: {self.consumer_group_id}, consumer_instance_id: {self.consumer_instance_id}"


class InferenceConfigurations:
    """Configurations for inference storage and processing.

    - Defines storage backend and windowing settings.
    - Uses RocksDB for persistence in production.
    """
    # Storage backend configuration (Default: in-memory, Recommended: RocksDB for production)
    store_host = str(os.getenv("STORE_HOST") or "memory://") # In production, "rocksdb://" should be used for persistence.
    # Inference windowing settings
    window_size = int(os.getenv("WINDOW_SIZE") or "2") # Window size in seconds
    overlap_size = int(os.getenv("OVERLAP_SIZE") or "1") # Overlap size in seconds
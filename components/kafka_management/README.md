# Kafka_Management
Kafka cluster management tools

## Sample Usage
1. Create a topic ("topic_1")
```bash
kafka-topics.sh --zookeeper ${ZOOKEEPER_HOST} --create --topic topic_1 --partitions 6 --replication-factor 3
```

2. Read from a topic ("topic_1")
```bash
kafka-console-consumer.sh --bootstrap-server ${KAFKA_HOST} --consumer.config ${KAFKA_CONFIG} --topic topic_1 --from-beginning
```

3. Write to a topic ("topic_1")
```bash
kafka-console-producer.sh --broker-list ${KAFKA_HOST} --producer.config ${KAFKA_CONFIG} --topic topic_1
```

4. List topics
```bash
kafka-topics.sh --zookeeper ${ZOOKEEPER_HOST} --list 
```

5. Delete a topic ("topic_1")
```bash
kafka-topics.sh --zookeeper ${ZOOKEEPER_HOST} --delete --topic topic_1
```
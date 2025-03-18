#!/bin/bash
# Kubernetes namespace for Kafka deployment
NAMESPACE=kafka-management
# Default Kafka topic name
TOPIC=topic_1
# Default number of partitions for topics
partitions=12

# Create required resources and deploy Kafka client
all:
	kubectl create namespace $(NAMESPACE) 2>/dev/null ; true
	kubectl create secret generic kafka-host -n $(NAMESPACE) \
  		--from-file=secret/kafka_host.txt --from-file=secret/zookeeper_host.txt 2>/dev/null ; true
	kubectl create secret generic kafka-secret -n $(NAMESPACE) \
  		--from-file=secret/client_sasl.properties 2>/dev/null ; true
	kubectl apply -f main.yaml

# Create a Kafka topic inside the Kafka client container
create-topic:
	kubectl exec -it -n kafka-management deploy/kafka-client -- sh -c \
	'kafka-topics.sh --zookeeper $${ZOOKEEPER_HOST} --create --topic ${TOPIC} --partitions ${partitions} --replication-factor 3'

# Delete an existing Kafka topic inside the Kafka client container
delete-topic:
	kubectl exec -it -n kafka-management deploy/kafka-client -- sh -c \
	'kafka-topics.sh --zookeeper $${ZOOKEEPER_HOST} --delete --topic ${TOPIC}'

# Create changelog topics required for Kafka Streams
create-changelog:
	make create-topic TOPIC=main-windowing_queue-changelog partitions=$(partitions)
	make create-topic TOPIC=main-__assignor-__leader partitions=$(partitions)

# Delete changelog topics for Kafka Streams
delete-changelog:
	make delete-topic TOPIC=main-windowing_queue-changelog
	make delete-topic TOPIC=main-__assignor-__leader

# Recreate changelog topics by deleting and creating them again
recreate-changelog:
	make delete-topic TOPIC=main-windowing_queue-changelog
	make delete-topic TOPIC=main-__assignor-__leader
	make create-topic TOPIC=main-windowing_queue-changelog partitions=$(partitions)
	make create-topic TOPIC=main-__assignor-__leader partitions=$(partitions)

# Recreate a Kafka topic by deleting and creating it again
recreate-topic:
	make delete-topic TOPIC=$(TOPIC) && make create-topic TOPIC=$(TOPIC) partitions=$(partitions)

# Recreate a Kafka topic along with its changelog topics
recreate-topic-with-changelog:
	make recreate-changelog partitions=$(partitions)
	make recreate-topic TOPIC=$(TOPIC) partitions=$(partitions)

# Clean up all resources in the specified namespace
clean:
	kubectl delete all --namespace $(NAMESPACE) --all
	kubectl delete namespace $(NAMESPACE)
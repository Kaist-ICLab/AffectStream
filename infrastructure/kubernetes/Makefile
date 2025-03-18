#!/bin/bash

PUB_NAMESPACE=producer
SUB_NAMESPACE=consumer

# Create required resources and deploy simulator, producer, and consumer
all:
	# kubectl create namespace $(PUB_NAMESPACE) 2>/dev/null ; true
	# kubectl create secret generic cloud-secret -n $(PUB_NAMESPACE) \
  	# 	--from-file=secret/cloud_user.txt,secret/cloud_passwd.txt,secret/kafka_host.txt
	# kubectl create namespace $(SUB_NAMESPACE) 2>/dev/null ; true
	# kubectl create secret generic cloud-secret -n $(SUB_NAMESPACE) \
  	# 	--from-file=secret/cloud_user.txt,secret/cloud_passwd.txt,secret/kafka_host.txt
	@cd simulator && make all 2>/dev/null ; true
	@cd producer && make all 2>/dev/null ; true
	@cd consumer && make all 2>/dev/null ; true

# Clean up all resources in the specified namespace
clean:
	@cd simulator && make clean 2>/dev/null ; true
	@cd producer && make clean 2>/dev/null ; true
	@cd consumer && make clean 2>/dev/null ; true
	# @kubectl delete namespace $(PUB_NAMESPACE) 2>/dev/null ; true
	# @kubectl delete namespace $(SUB_NAMESPACE) 2>/dev/null ; true

# Create required resources and deploy analysis and kafka-management
start:
	@cd analysis && make all 2>/dev/null ; true
	@cd kafka-management && make all 2>/dev/null; true

# Create kafka topic and changelog
start-topic:
	@cd kafka-management && make create-topic && make create-changelog 2>/dev/null ; true

# Clean up all resources in the specified namespace
end:
	@cd analysis && make clean && make all 2>/dev/null ; true
	@cd kafka-management && make recreate-topic-with-changelog 2>/dev/null ; true

# Clean up all resources in the specified namespace
finish:
	@cd analysis && make clean 2>/dev/null ; true
	@cd kafka-management && make clean 2>/dev/null ; true
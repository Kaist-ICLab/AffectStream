#!/bin/bash
NAMESPACE=producer
replicas=1

# Create required resources and deploy producer
all:
	kubectl create namespace $(NAMESPACE) 2>/dev/null ; true
	kubectl create secret generic cloud-secret -n $(NAMESPACE) \
  		--from-file=secret/cloud_user.txt,secret/cloud_passwd.txt,secret/kafka_host.txt 2>/dev/null ; true
	kubectl apply -f svc-account.yaml
	kubectl apply -f main.yaml

# Scale the producer deployment
scale:
	kubectl scale deploy/producer --namespace $(NAMESPACE) --replicas=$(replicas)

# Clean up all resources in the specified namespace
clean:
	kubectl delete all --namespace $(NAMESPACE) --all
	kubectl delete namespace $(NAMESPACE)
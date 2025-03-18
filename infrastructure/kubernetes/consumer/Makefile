#!/bin/bash
NAMESPACE=subscriber
replicas=1

# Create a namespace and secret, then deploy the application
all:
	kubectl create namespace $(NAMESPACE) 2>/dev/null ; true
	kubectl create secret generic cloud-secret -n $(NAMESPACE) \
  		--from-file=secret/cloud_user.txt,secret/cloud_passwd.txt,secret/kafka_host.txt,secret/iam_access_key_id.txt,secret/iam_secret_access_key.txt 2>/dev/null ; true
	kubectl apply -f main.yaml

# Scale the application
scale:
	kubectl scale deploy/subscriber --namespace $(NAMESPACE) --replicas=$(replicas)

# Delete the application and namespace
clean:
	kubectl delete all --namespace $(NAMESPACE) --all
	kubectl delete namespace $(NAMESPACE)
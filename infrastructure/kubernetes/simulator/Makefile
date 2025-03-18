#!/bin/bash
NAMESPACE=simulator
replicas=1
max_user=100
spawn_rate=10
duration=10
partitions=6
consumer_replicas=6

# Create required resources and deploy simulator
all:
	kubectl create namespace $(NAMESPACE) 2>/dev/null ; true
	kubectl apply -f master.yaml
	kubectl apply -f worker.yaml

# Scale the simulator deployment
scale:
	kubectl scale deploy/worker --namespace $(NAMESPACE) --replicas=$(replicas)

# Get the current state of the simulator
get-state:
	kubectl exec -it -n ${NAMESPACE} deploy/master -- sh -c "curl 'http://localhost:8089/stats/requests' -H 'X-Requested-With: XMLHttpRequest'" | python -c "import sys,json; print(json.load(sys.stdin)['stats'][0])"

# Simulate user activity
simulate:
	kubectl exec -it -n ${NAMESPACE} deploy/master -- sh -c \
	"curl -X POST http://localhost:8089/swarm \
	-H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
	-H 'X-Requested-With: XMLHttpRequest' \
	-d 'user_count='$(max_user)'&spawn_rate='${spawn_rate}'&host='http://producer.producer:8080''"
	sleep ${duration}
	kubectl exec -it -n ${NAMESPACE} deploy/master -- sh -c "curl -X GET http://localhost:8089/stop"

# Full simulation
full-simulate:
	cd ../analysis && kubectl apply -f main.yaml && cd ../simulator
	cd ../kafka-management && make recreate-topic-with-changelog partitions=$(partitions) && cd ../simulator
	cd ../ && make all && cd simulator
	cd ../subscriber && make scale replicas=$(consumer_replicas)
	make scale replicas=$(replicas)
	echo "waiting for compoenents to be ready" && sleep 20
	make simulate max_user=$(max_user) spawn_rate=$(spawn_rate) duration=$(duration)
	cd ../subscriber && kubectl delete deployment -n subscriber subscriber && cd ../simulator
	kubectl get svc -n analysis | grep "elb.amazonaws.com"

# Clean up all resources in the specified namespace
post-simulate:
	cd ../ && make clean && cd simulator
	cd ../analysis && kubectl delete deployment -n analysis db && cd ../simulator

# Clean up all resources in the specified namespace
clean:
	kubectl delete all --namespace $(NAMESPACE) --all
	kubectl delete namespace $(NAMESPACE)

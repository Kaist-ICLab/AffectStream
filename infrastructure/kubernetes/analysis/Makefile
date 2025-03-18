#!/bin/bash
NAMESPACE=analysis
replicas=1

all:
	kubectl create namespace $(NAMESPACE) 2>/dev/null ; true
	kubectl create configmap db-init --namespace $(NAMESPACE) --from-file init.sql 2>/dev/null ; true
	kubectl apply -f main.yaml

dump:
	kubectl exec -it -n ${NAMESPACE} deploy/db -- sh -c \
	'pg_dump public -w > /tmp/latency_result.sql'
	kubectl cp -n ${NAMESPACE} deploy/db:/tmp/latency_result.sql latency_result.sql

clean:
	kubectl delete all --namespace $(NAMESPACE) --all
	kubectl delete namespace $(NAMESPACE)
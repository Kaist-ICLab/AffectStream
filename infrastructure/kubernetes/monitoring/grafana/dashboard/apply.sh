#!/usr/bin/env bash

JSONNET_PATH=grafonnet-lib \
  jsonnet -J ./vendor dashboard.jsonnet > dashboard.json

payload="{\"dashboard\": $(jq . dashboard.json), \"overwrite\": true}"

curl -X POST --user "admin:admin" \
  -H 'Content-Type: application/json' \
  -d "${payload}" \
  "http://34.22.71.205:3000/api/dashboards/db"

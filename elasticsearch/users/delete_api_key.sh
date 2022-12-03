#!/usr/bin/env sh

url="https://localhost:9200"

id=$(jq -r '.id' api_key.json)

curl -n \
    -H 'Content-Type: application/json' \
    -XDELETE "$url/_security/api_key?pretty" \
    -d '
{
  "name" : "my_api_key"
}
'



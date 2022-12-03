#!/usr/bin/env sh

id=$(jq -r '.id' api_key.json)
api_key=$(jq -r '.api_key' api_key.json)
encoded=$(jq -r '.encoded' api_key.json)

#encoded=$(echo -n "$id:$api_key" | base64)

url="https://192.168.0.98:9200"

curl -n \
    -H "Authorization: ApiKey $encoded" \
    -H 'Content-Type: application/json' \
    -XGET "$url?pretty"


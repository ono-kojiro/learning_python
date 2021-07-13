#!/bin/sh

username=elastic
password=XXXXXXXXXXXXXXXXXXXX

server="$username:$password@192.168.0.98:9200"

curl \
    -H 'Content-Type: application/x-ndjson' \
	-X DELETE https://$server/_security/api_key \
	-d '
{
  "name": "my-api-key"
}
'



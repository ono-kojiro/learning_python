#!/bin/sh

username=elastic
password=XXXXXXXXXXXXXXXXXXXX
	
server="$username:$password@192.168.0.98:9200"

curl \
    -H 'Content-Type: application/x-ndjson' \
	-X POST https://$server/_security/api_key \
	-d '
{
  "name": "my-api-key",
  "expiration": "1d", 
  "metadata": {
    "application": "my-application",
    "environment": {
       "level": 1,
       "trusted": true,
       "tags": ["dev", "staging"]
    }
  }
}
'


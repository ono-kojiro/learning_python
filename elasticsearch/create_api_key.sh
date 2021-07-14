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
' | tee api_key.json

id=`jq -r '.id' api_key.json`
api_key=`jq -r '.api_key' api_key.json`

echo ""

echo "id : $id"
echo "api_key : $api_key"

str="$id:$api_key"
echo "input is $str"

api_key=`echo -n "$id:$api_key" | base64`

echo "base64 : $api_key"

curl \
        -H "Authorization: ApiKey $api_key" \
        https://192.168.0.98:9200/



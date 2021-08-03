#!/bin/sh

username=elastic
password=`cat password.txt | grep "PASSWORD elastic" | gawk '{ print $4 }'`
	
server="$username:$password@192.168.0.98:9200"

curl \
    -H 'Content-Type: application/x-ndjson' \
	-X DELETE https://$server/_security/api_key \
	-d '
{
  "name": "myname"
}
'



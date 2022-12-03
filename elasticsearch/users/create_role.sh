#!/usr/bin/env sh

name="my_admin_role"

url="https://localhost:9200"

curl -n \
    -H 'Content-Type: application/json' \
    -XPUT "$url/_security/role/${name}?pretty" \
    -d '
{
  "cluster": ["all"],
  "indices": [
    {
      "names": [ "*" ], 
      "privileges": ["write","create","create_index","manage","manage_ilm"]  
    }
  ]
}
'


#!/usr/bin/env sh

name="my_api_key"
roles="my_admin_role"

rm -f api_info.json

cat - << EOS >> api_info.json
{
  "name" : "${name}",
  "role_descriptors" : {
    "role1" : {
      "cluster": ["all"],
      "index" : [
        {
           "names" : ["*"],
           "privileges" : ["read"]
        }
      ]
    },
    "role2" : {
      "cluster": ["all"],
      "index" : [
        {
           "names" : ["myindex-*"],
           "privileges" : ["all"]
        }
      ]
    }
  }
}
EOS

url="https://localhost:9200"

curl -n \
    -H 'Content-Type: application/json' \
    -XPOST "$url/_security/api_key?pretty" \
    -d @api_info.json \
    > api_key.json

rm -f api_info.json


#!/usr/bin/env sh

username="$USER"

rm -f user_info.json

url="https://localhost:9200"

curl -n \
    -H 'Content-Type: application/json' \
    -XDELETE "$url/_security/user/$username?pretty"


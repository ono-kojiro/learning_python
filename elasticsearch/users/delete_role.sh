#!/usr/bin/env sh

name="my_admin_role"

url="https://localhost:9200"

curl -n \
    -H 'Content-Type: application/json' \
    -XDELETE "$url/_security/role/${name}?pretty"


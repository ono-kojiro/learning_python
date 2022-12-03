#!/usr/bin/env sh


url="https://192.168.0.98:9200"

curl -n \
    -H 'Content-Type: application/json' \
    -XGET "$url?pretty"


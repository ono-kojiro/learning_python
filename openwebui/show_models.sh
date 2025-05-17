#!/bin/sh

# define api_key
. ./api_key.shrc

# define base_url
. ./config.shrc

curl -s -k \
    -H "Authorization: Bearer ${api_key}" \
    ${base_url}/api/models | \
    jq .data[].name



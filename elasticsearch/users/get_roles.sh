#!/usr/bin/env sh


adminname=$(cat ../.netrc | grep login | gawk '{ print $2 }')
adminpass=$(cat ../.netrc | grep password | gawk '{ print $2 }')

url="https://localhost:9200"

curl \
    -H 'Content-Type: application/json' \
    -XGET "$url/_security/role?pretty" \
    -u ${adminname}:${adminpass}


#!/usr/bin/env sh


adminname=$(cat ../.netrc | grep login | gawk '{ print $2 }')
adminpass=$(cat ../.netrc | grep password | gawk '{ print $2 }')

url="https://localhost:9200"

curl -n \
    -H 'Content-Type: application/json' \
    -XGET "$url/_security/user?pretty"

#-u ${adminname}:${adminpass}


#!/usr/bin/env sh

username="$USER"
password="secret"

full_name=$(git config --get user.name)

roles="my_admin_role"

rm -f user_info.json

cat - << EOS >> user_info.json
{
  "password" : "${password}",
  "roles" : [ "$roles" ],
  "full_name" : "${full_name}"
}
EOS

url="https://localhost:9200"

curl -n \
    -H 'Content-Type: application/json' \
    -XPOST "$url/_security/user/$username?pretty" \
    -d @user_info.json

rm -f user_info.json


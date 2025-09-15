#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

ret=0

netrc="${top_dir}/.netrc"
machine=`cat $netrc | grep -e '^machine' | awk '{ print $2 }'`
es_url="https://${machine}:9200"

echo "INFO: use ${netrc}"
echo "INFO: url is ${es_url}"

help() {
  cat - << EOS
usage : $0 <TARGET>

  target:
    createkey
    deletekey
    listkey
  
    debug
EOS
}

usage()
{
  help
}

clean()
{
  :
}

debug()
{
  curl -k --netrc-file ${netrc} ${es_url}
}

createkey()
{
  cat - << EOF > _data.json
{
  "name": "myuser",
  "role_descriptors": {
    "myrole" : {
      "cluster": ["all"],
      "indices": [
        {
          "names": ["*"],
          "privileges": ["all"]
        }
      ]
    }
  },
  "metadata": {
    "application": "myapplication",
    "environment": {
       "level": 1,
       "trusted": true,
       "tags": ["dev", "staging"]
    }
  }
}
EOF

  cmd="curl -k --silent --netrc-file ${netrc}"
  cmd="$cmd -H 'Content-Type: application/json'"
  cmd="$cmd -X POST ${es_url}/_security/api_key?pretty"
  cmd="$cmd -d @_data.json"
  echo $cmd

  eval $cmd > api_key.json
  rm -f _data.json
}

deletekey()
{
  name=`cat api_key.json | jq -r '.name'`
  echo $name
  curl -k --silent --netrc-file ${netrc} \
    -H 'Content-Type: application/json' \
    -X DELETE ${es_url}/_security/api_key?pretty --data @- << EOF
{
  "name": "${name}"
}
EOF

}

listkey()
{
  curl \
    -k \
    --silent \
    --netrc-file ${netrc} \
    -H 'Content-Type: application/json' \
    -X GET ${es_url}/_security/api_key?pretty |
  jq -r '.api_keys.[] | select(.invalidated == false)
    | { id: .id, name: .name }'
}

indices() {
  curl -k --netrc-file $netrc "$es_url/_cat/indices?v"
}

tables() {
  indices
}

alias() {
  # ignore dot (".") index
  curl -k --silent --netrc-file $netrc "$es_url/_aliases?pretty" | \
          jq -r 'keys | .[] | select(. | test("^[^.]"))'
}

test() {
  curl -k --silent --netrc-file $netrc \
    -H 'Content-Type: application/json' \
    "$es_url/packetbeat-*/_search?pretty" \
    --data @- << EOF 
{
  "size": 10,
  "_source": ["@timestamp", "source.ip.keyword", "source.bytes", "destination.ip" ]
}
EOF

}

test2() {
  curl -k --silent --netrc-file $netrc \
    -H 'Content-Type: application/json' \
    "$es_url/packetbeat-*/_search?pretty" \
    --data @- << EOF 
{
  "size": 0,
  "aggs": {
    "table": {
      "composite": {
        "size": 100,
        "sources": [
          {
             "stk1": {
               "terms": { "field": "source.ip.keyword" }
             }
          },
          {
             "stk2": {
               "terms": { "field": "destination.ip.keyword" }
             }
          }
        ]
      }
    }
  }
}
EOF

}

all()
{
  create
  password
  version
  delete
}

args=""

username=""
password=""
fullname=""
email=""

while [ $# -ne 0 ]; do
  case "$1" in
    -h )
      usage;;
    -v )
      verbose=1;;
    -l )
      shift
      logfile=$1;;
    -u | --username )
      shift
      username=$1;;
    -p | --password )
      shift
      password=$1;;
    *)
      args="$args $1"
  esac

  shift
done

#if [ -z "$password" ]; then
#  echo "no password option"
#  ret=`expr $ret + 1`
#fi

if [ $ret -ne 0 ]; then
  usage
  exit $ret
fi

#if [ $# -eq 0 ]; then
#  create
#  exit
#fi

if [ -z "$args" ]; then
  usage
  exit 1
fi



for arg in $args ; do
  num=`LANG=C type $arg | grep 'function' | wc -l`

  if [ $num -ne 0 ]; then
    $arg
  else
    echo "no such function, $arg"
    exit 1
  fi
done


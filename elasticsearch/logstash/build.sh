#!/bin/sh

set -e

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

es_host="https://192.168.0.98:9200"
netrc="${top_dir}/../.netrc"

ret=0

if [ ! -e "$netrc" ]; then
  echo "ERROR : no netrc, $netrc"
  ret=`expr $ret + 1`
fi

if [ $ret -ne 0 ]; then
  exit $ret
fi

help() {
  cat - << EOS
usage : $0 <command>
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

# REST APIs
# https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html

fetch()
{
  url="https://download.elastic.co/demos/kibana/gettingstarted/logs.jsonl.gz"
  if [ ! -e "logs.jsonl.gz" ]; then
    wget $url
  fi
  
  if [ ! -e "logs.jsonl" ]; then
    gunzip -k logs.jsonl.gz
  fi

  sed -i.bak -e 's|,"_type":".*"||' logs.jsonl
}

mapping()
{
  dates="2015.05.18 2015.05.19 2015.05.20"

  for dt in $dates; do
    curl -k --netrc-file $netrc \
      -H 'Content-Type: application/json' \
      -XPUT "$es_host/logstash-${dt}?pretty" \
      --data-binary @- << EOS
{
  "mappings": {
    "properties": {
      "geo": {
        "properties": {
          "coordinates": {
            "type": "geo_point"
          }
        }
      }
    }
  }
}
EOS

  done
}

post()
{
  curl -k --netrc-file $netrc \
    -H 'Content-Type: application/json' \
    -XPOST "$es_host/_bulk?pretty" \
    --data-binary "@logs.jsonl"
}

delete()
{
  # enable following line in /etc/elasticsearch/elasticsearch.yml
  # if you want to use wildcards
  #action.destructive_requires_name: false
  curl -k --netrc-file $netrc \
    -XDELETE "$es_host/logstash-*?expand_wildcards=all" 
}

indices()
{
  curl -k --netrc-file $netrc \
    "$es_host/_cat/indices?v"
}


all()
{
  fetch
}

args=""

while [ $# -ne 0 ]; do
  case "$1" in
    -h )
      usage;;
    -v )
      verbose=1;;
    -l )
      shift
      logfile=$1;;
    *)
      args="$args $1"
  esac

  shift
done

if [ -z "$args" ]; then
  help
  exit 0
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


#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

es_host="192.168.0.98:9200"
kibana_host="192.168.0.98:5601"

ret=0

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
  curl -O -L \
    https://download.elastic.co/demos/kibana/gettingstarted/accounts.zip
}

post()
{
  curl -n \
    -H 'Content-Type: application/json' \
    -XPOST "https://${es_host}/bank/_bulk?pretty" \
    --data-binary "@accounts.json"
}

doc()
{
  #curl -n -XGET "https://${es_host}/bank/_doc/995"
  curl -n -XGET "https://${es_host}/bank/_search?pretty=true&q=*:*"
}


delete()
{
  curl -n -XDELETE "https://${es_host}/bank?pretty"
}

all()
{
  :
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

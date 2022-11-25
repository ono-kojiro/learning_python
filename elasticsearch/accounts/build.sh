#!/bin/sh

set -e

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

es_host="https://192.168.0.98:9200"
kibana_host="https://192.168.0.98:5601"

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

post()
{
  curl -k --netrc-file $netrc \
    -H 'Content-Type: application/json' \
    -XPOST "$es_host/bank/_bulk?pretty" \
    --data-binary "@accounts.json"
}

delete()
{
  curl -k --netrc-file $netrc \
    -XDELETE "$es_host/bank?pretty" 
}

data_views()
{
  curl -k --netrc-file $netrc \
    -XGET "$kibana_host/api/data_views"
}

spaces()
{
  curl -k --netrc-file $netrc \
    -XGET "$kibana_host/api/spaces/space"
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


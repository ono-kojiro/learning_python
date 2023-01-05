#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd ${top_dir}

es_host="192.168.0.98:9200"
kibana_host="192.168.0.98:5601"

index="my_index-1000"
pretty="?pretty"

data_view="my_data_view"

ret=0

help() {
  cat - << EOS
usage : $0 <command>

  command
    help

  document and index:
    add, get, delete,
    indices, delete_index

  data view:
    create_dataview, get_dataview, delete_dataview
    get_dataviews
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

version()
{
  curl -n "https://${es_host}"
}

add()
{
  id="simple"
  curl -n \
    -H 'Content-Type: application/json' \
    -XPOST "https://${es_host}/${index}/_bulk" \
    --data-binary @- << EOS

{ "index": {"_id": "${id}"} }
{ "name" : "aaa", "value" : 1 }

EOS
}

get()
{
  pretty=""
  id="simple"
  curl -n -XGET "https://${es_host}/${index}/_doc/${id}${pretty}"
}

delete()
{
  id="simple"
  curl -n -XDELETE "https://${es_host}/${index}/_doc/${id}${pretty}"
}

delete_index()
{
  indices="${index}"
  for idx in ${indices}; do
    curl -n -XDELETE "https://${es_host}/${idx}"
  done
}

create_dataview()
{
  curl -n \
      -H 'Content-Type: application/json' \
    -H "kbn-xsrf: reporting" \
    -XPOST "https://${kibana_host}/kibana/api/data_views/data_view?pretty" \
    --data-binary @- << EOS
{
  "data_view" : {
    "id"    : "${data_view}",
    "version" : "0.0.1",
    "title" : "my_index-*",
    "name"  : "My Data View"
  }
}
EOS

}

get_dataview()
{
  curl -n \
    -H 'Content-Type: application/json' \
    -XGET "https://${kibana_host}/kibana/api/data_views/data_view/${data_view}?pretty=true" 
}

get_dataviews()
{
  curl -n \
    -H "kbn-xsrf: reporting" \
    -XGET "https://${kibana_host}/kibana/api/data_views?pretty"
}


delete_dataview()
{
    #-H 'Content-Type: application/json' \
  curl -n \
    -H "kbn-xsrf: reporting" \
    -XDELETE "https://${kibana_host}/kibana/api/data_views/data_view/${data_view}" 
}



indices()
{
  curl -n "https://${es_host}/_cat/indices?v"
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

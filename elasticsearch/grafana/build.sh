#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

es_url="https://192.168.0.98:9200"
kibana_url="https://192.168.0.98:5601/kibana"
#kibana_url="https://192.168.0.98/kibana"

dt_str=$(date +"%Y.%m.%d")

index="mymetrics-${dt_str}"

ret=0

help() {
  cat - << EOS
usage : $0 <command>

  generate        generate jsonl
  post            post jsonl
  delete          delete index

EOS
}

version()
{
  curl -n "${es_url}"
}

usage()
{
  help
}

clean()
{
  :
}

cpu()
{
  jsonl="${index}.jsonl"
  echo "generate ${jsonl}"
  #./generate.py > ${jsonl}
  count=0
  while [ "$count" -lt 3600 ]; do
    echo count is $count
    python3 cpu_usage.py -i ${index} -o ${index}.jsonl -n 1
    curl -k -n --silent \
      -H 'Content-Type: application/json' \
      -XPOST "${es_url}/${index}/_bulk?pretty" \
      --data-binary "@${index}.jsonl" > /dev/null

    python3 mem_usage.py -i ${index} -o ${index}.jsonl -n 1
    curl -k -n --silent \
      -H 'Content-Type: application/json' \
      -XPOST "${es_url}/${index}/_bulk?pretty" \
      --data-binary "@${index}.jsonl" > /dev/null

    count=$(expr $count + 1)
  done
}

generate()
{
  jsonl="${index}.jsonl"
  echo "generate ${jsonl}"
  #./generate.py > ${jsonl}
  python3 cpu_usage.py -i ${index} -o ${index}.jsonl -n 60
}

gen()
{
  generate
}

post()
{
  #dt_str=$(date +"%Y%m%d-%H%M%S")

  curl -k -n \
    -H 'Content-Type: application/json' \
    -XPOST "${es_url}/${index}/_bulk?pretty" \
    --data-binary "@${index}.jsonl"
}

delete()
{
  #index="mymetrics-20230218-105718"
  curl -n -XDELETE "${es_url}/${index}?pretty"

}

views()
{
  # get all data views
  curl -n \
    -X GET \
    "${kibana_url}/api/data_views?pretty" | python3 -mjson.tool
}

del_view()
{
  #view="mymetrics-*"
  id="0b7c21b4-7527-4227-8aeb-89a1752ef486"

  curl -n -X DELETE \
    -H 'Content-Type: application/json' \
    -H 'kbn-xsrf: reporting' \
    "${kibana_url}/api/data_views/data_view/${id}"
}

spaces()
{
  
  curl -n \
    -XGET "${kibana_url}/api/spaces/space"
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


#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

# https://www.elastic.co/guide/jp/kibana/current/tutorial-load-dataset.html
# https://qiita.com/rjkuro/items/95f71ad522226dc381c8
# https://www.elastic.co/jp/blog/strings-are-dead-long-live-strings

# Elasticsearch as a NoSQL Database
# https://www.elastic.co/jp/blog/found-elasticsearch-as-nosql

# RDB      :  elasticsearch
# database => index
# table    => mapping type
# column   => field
# record   => doc

server="localhost:9200"

mclean() {
  rm -f shakespeare.json
  rm -f accounts.zip
  rm -f logs.jsonl.gz
}

clean() {
  rm -f accounts.json
  rm -f logs.jsonl
}

fetch() {
  wget https://download.elastic.co/demos/kibana/gettingstarted/shakespeare.json
  wget https://download.elastic.co/demos/kibana/gettingstarted/accounts.zip
  wget https://download.elastic.co/demos/kibana/gettingstarted/logs.jsonl.gz
}


expand() {
  if [ ! -e accounts.json ]; then
    echo "expand accounts.zip"
    unzip accounts.zip
  else
    echo "accounts.json already exists."
  fi

  if [ ! -e logs.jsonl ]; then
    echo "expand logs.jsonl.gz"
    gunzip logs.jsonl.gz
  else
    echo "logs.jsonl already exists."
  fi
}

mapping() {
  mapping_shakespeare
  mapping_logstash
}

mapping_shakespeare() {

  curl \
    -H 'Content-Type: application/json' \
    -XPUT http://localhost:9200/shakespeare \
    -d '
{
 "mappings" : {
  "_default_" : {
   "properties" : {
    "speaker" : {"type": "keyword", "index" : true },
    "play_name" : {"type": "keyword", "index" : true },
    "line_id" : { "type" : "integer" },
    "speech_number" : { "type" : "integer" }
   }
  }
 }
}
';

}

mapping_logstash() {
  dates="2015.05.18 2015.05.19 2015.05.20"

  for dt in $dates; do
    curl \
      -H 'Content-Type: application/json' \
      -XPUT http://localhost:9200/logstash-${dt} \
      -d '
{
  "mappings": {
    "log": {
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
}
';
  done

}

unmapping() {
  unmapping_shakespeare
  unmapping_logstash
}

unmapping_shakespeare() {
  curl -XDELETE 'localhost:9200/shakespeare?pretty'
}

unmapping_logstash() {
  dates="2015.05.18 2015.05.19 2015.05.20"

  for dt in $dates; do
    curl -XDELETE "localhost:9200/logstash-${dt}?pretty"
  done
}

indices() {
  curl "$server/_cat/indices?v"
}

import() {
  curl \
    -H 'Content-Type: application/x-ndjson' \
    -XPOST 'localhost:9200/bank/account/_bulk?pretty' \
    --data-binary @accounts.json

  curl \
    -H 'Content-Type: application/x-ndjson' \
    -XPOST 'localhost:9200/shakespeare/_bulk?pretty' \
    --data-binary @shakespeare.json

  curl \
    -H 'Content-Type: application/x-ndjson' \
    -XPOST 'localhost:9200/_bulk?pretty' \
    --data-binary @logs.jsonl
}

#curl -XDELETE 'localhost:9200/logstash-2015.05.18?pretty'

if [ "x$@" = "x" ]; then
  usage
  exit
fi

logfile=""

while getopts hvl: option
do
    case "$option" in
        h)
            usage;;
        v)
            verbose=1;;
        l)
            logfile=$OPTARG;;
        *)
            echo unknown option "$option";;
    esac
done

shift $(($OPTIND-1))

if [ "x$logfile" != "x" ]; then
    echo logfile is $logfile
fi

for target in "$@" ; do
    LANG=C type $target | grep function > /dev/null 2>&1
    res=$?
    if [ "x$res" = "x0" ]; then
        $target
    else
		echo "no such function, $target"
		exit 1
    fi
done


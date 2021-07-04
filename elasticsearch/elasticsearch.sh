#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

# https://www.elastic.co/guide/jp/kibana/current/tutorial-load-dataset.html
# https://www.elastic.co/guide/jp/kibana/current/tutorial-define-index.html

# https://qiita.com/rjkuro/items/95f71ad522226dc381c8
# https://www.elastic.co/jp/blog/strings-are-dead-long-live-strings

# Elasticsearch as a NoSQL Database
# https://www.elastic.co/jp/blog/found-elasticsearch-as-nosql

# https://ameblo.jp/shinnaka54/entry-12407824098.html

# https://qiita.com/ground0state/items/e118c1970fca70518f6e

# RDB      :  elasticsearch
# database => index
# table    => mapping type
# column   => field
# record   => doc

es_host="localhost:9200"
kibana_host="localhost:5601"

help() {
  echo "usage : $0 <subcommand>"
  echo ""
  echo "  subcommand"
  echo "    help"
  echo ""
  echo "    fetch"
  echo "    expand"
  echo ""
  echo "    mapping"
  echo "    unmapping"
  echo ""
  echo "    import"
  echo "    indices"
  echo ""
  echo "    clean"
  echo "    mclean"
}

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
  demo_url=https://download.elastic.co/demos/kibana/gettingstarted
  filenames="shakespeare.json accounts.zip logs.jsonl.gz"
  for filename in $filenames; do
    if [ ! -e $filename ]; then
      wget $demo_url/$filename
    else
      echo "skip $filename"
    fi
  done
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
  unmapping_bank
  unmapping_logstash
}

unmapping_shakespeare() {
  curl -XDELETE 'localhost:9200/shakespeare?pretty'
}

unmapping_bank() {
  curl -XDELETE 'localhost:9200/bank?pretty'
}

unmapping_logstash() {
  dates="2015.05.18 2015.05.19 2015.05.20"

  for dt in $dates; do
    curl -XDELETE "localhost:9200/logstash-${dt}?pretty"
  done
}

indices() {
  curl "$es_host/_cat/indices?v"
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

create_index_pattern() {
  curl \
      -H 'Content-Type: application/json' \
      -XPOST "$es_host/index_patterns/index_pattern" \
    -d '
{
  "index_pattern": {
    "title": "shakes*"
  }
}
';

  curl \
      -H 'Content-Type: application/json' \
      -XPOST "$es_host/index_patterns/index_pattern" \
    -d '
{
  "ban*": {
    "title": "hello"
  }
}
';

}

create() {
  curl -X PUT "$es_host/sample_index"
}

alias() {
  curl "$es_host/_aliases?pretty"
}

settings() {
  curl "$es_host/sample_index/_settings?pretty"
}

insert() {
  type=mytype
  doc=1
  curl \
    -H 'Content-Type: application/json' \
    -X POST "$es_host/sample_index/$type/$doc" \
    -d '
{
  "title" : "sample no.1",
  "description" : "This is a sample data",
  "tag" : [ "elasticsearch", "search-engine"],
  "no"   : 3,
  "ratio" : 0.53,
  "enabled" : true
}
';

}

confirm_mapping() {
  type=mytype
  doc=1
  curl \
    "$es_host/sample_index/_mapping/$type?pretty"

}

confirm_data() {
  type=mytype
  doc=1
  curl \
    "$es_host/sample_index/$type/$doc?pretty"

}


delete() {
  curl -X DELETE "$es_host/sample_index"
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


#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

# $ sudo vi /etc/elasticsearch/elasticsearch.yml
# node.name: node-1
# network.host: 192.168.0.98
# discovery.seed_hosts: ["192.168.0.98"]
# cluster.initial_master_nodes: ["node-1"]

# $ sudo vi /etc/kibana/kibana.yml
# server.host: "0.0.0.0"
# elasticsearch.hosts: ["http://192.168.0.98:9200"]


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

es_host="192.168.0.98:9200"
kibana_host="192.168.0.98:5601"

help() {
  echo "usage : $0 <subcommand>"
  echo ""
  echo "  demo"
  echo "    fetch/expand"
  echo "    mapping/unmapping"
  echo "    import/indices"
  echo ""
  echo "    clean/mclean"
  echo "    mclean"
  echo ""
  echo "  sample_index"
  echo "    create/destroy"
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

connect() {
  cmd="curl http://$es_host"
  echo $cmd
  $cmd
}

mapping() {
  mapping_shakespeare
  mapping_logstash
}

mapping_shakespeare() {

  curl \
    -H 'Content-Type: application/json' \
    -XPUT "$es_host/shakespeare?pretty" \
    -d '
{
  "mappings" : {
    "properties" : {
      "speaker" : {"type": "keyword", "index" : true },
      "play_name" : {"type": "keyword", "index" : true },
      "line_id" : { "type" : "integer" },
      "speech_number" : { "type" : "integer" }
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
      -XPUT "$es_host/logstash-${dt}?pretty" \
      -d '
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
';
  done

}

unmapping() {
  unmapping_shakespeare
  unmapping_bank
  unmapping_logstash
}

unmapping_shakespeare() {
  curl -XDELETE "$es_host/shakespeare?pretty"
}

unmapping_bank() {
  curl -XDELETE "$es_host/bank?pretty"
}

unmapping_logstash() {
  dates="2015.05.18 2015.05.19 2015.05.20"

  for dt in $dates; do
    curl -XDELETE "$es_host/logstash-${dt}?pretty"
  done
}

indices() {
  cmd="curl http://$es_host/_cat/indices?v"
  echo $cmd
  $cmd
}

tables() {
  indices
}


import() {
  curl \
    -H 'Content-Type: application/x-ndjson' \
    -XPOST "$es_host/bank/account/_bulk?pretty" \
    --data-binary @accounts.json

  curl \
    -H 'Content-Type: application/x-ndjson' \
    -XPOST "$es_host/shakespeare/_bulk?pretty" \
    --data-binary @shakespeare.json

  curl \
    -H 'Content-Type: application/x-ndjson' \
    -XPOST "$es_host/_bulk?pretty" \
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
  "tags" : [ "elasticsearch", "search-engine"],
  "no"   : 3,
  "ratio" : 0.53,
  "enabled" : true
}
';
  
  type=mytype
  doc=2
  curl \
    -H 'Content-Type: application/json' \
    -X POST "$es_host/sample_index/$type/$doc" \
    -d '
{
  "title" : "sample no.1",
  "description" : "This is a sample data",
  "tags" : [ "hoge", "foo", "bar" ],
  "no"   : 4,
  "ratio" : 0.931,
  "enabled" : false
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

search() {
  type=mytype
  doc=1
  curl \
    "$es_host/sample_index/$type/_search?q=tags:elasticsearch&pretty=true"

}

query() {
  curl \
    -H 'Content-Type: application/json' \
    -X POST "$es_host/bank/_search?pretty" \
    -d '
{
  "query": {
    "bool" : {
      "must" : [
        {
          "range" : {
            "account_number" : { "lt" : 100 }
          }
        },
        {
          "range" : {
            "balance" : { "gt" : 47500 }
          }
        }
      ]
    }
  }
}
';

}

destroy() {
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


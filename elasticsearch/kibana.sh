#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

# RDB      :  elasticsearch
# database => index
# table    => mapping type
# column   => field
# record   => doc

#kibana_host="192.168.0.98:5601"
kibana_host="localhost:5601"

help() {
  echo "usage : $0 <subcommand>"
  echo ""
  echo "  subcommand"
  echo "    help"
  echo ""
  echo "    create_index_pattern"
}

get_default_index_pattern() {
  curl \
      -H 'Content-Type: application/json' \
      -X GET "$kibana_host/api/index_patterns/default"
}


create_index_pattern() {
  index_pattern="api/saved_objects/index-pattern"

  curl \
    -H 'kbn-xsrf: true' \
    -H 'Content-Type: application/json' \
    -XPOST "$kibana_host/$index_pattern/myindex" \
    -d '
{
  "attributes": {
    "title": "logstash-*"
  }
}
';
  
  curl \
    -H 'kbn-xsrf: true' \
    -H 'Content-Type: application/json' \
    -XPOST "$kibana_host/$index_pattern/mybank" \
    -d '
{
  "attributes": {
    "title": "ba*"
  }
}
';


}

delete_index_pattern() {
  index_pattern="api/saved_objects/index-pattern"
  curl \
    -H 'kbn-xsrf: true' \
    -H 'Content-Type: application/json' \
    -XDELETE "$kibana_host/$index_pattern/myindex"
  curl \
    -H 'kbn-xsrf: true' \
    -H 'Content-Type: application/json' \
    -XDELETE "$kibana_host/$index_pattern/mybank"

}

all_spaces() {
  curl \
      -H 'Content-Type: application/json' \
      -X GET "$kibana_host/api/spaces/space"
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


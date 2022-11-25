#!/bin/bash

set -e

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

es_host="https://192.168.0.98:9200"

admin_netrc="${top_dir}/../.netrc"

curl="curl -k --netrc-file ${top_dir}/../.netrc"

ret=0

if [ ! -e "$admin_netrc" ]; then
  echo "ERROR : no admin netrc, $admin_netrc"
  ret=`expr $ret + 1`
fi

if [ $ret -ne 0 ]; then
  exit $ret
fi

help() {
  cat - << EOS
usage : $0 -u <username>
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

create()
{
  curl -k --netrc-file $admin_netrc \
    -H 'Content-Type: application/json' \
    -XPOST "$es_host/_security/user/$username?pretty" --data @- << EOS
{
  "password" : "$password",
  "enabled" : true,
  "roles" : [ "superuser", "kibana_admin" ],
  "full_name" : "$fullname",
  "email" : "$email",
  "metadata" : {
    "intelligence" : 7
  }
}
EOS

}

delete()
{
  curl -k --netrc-file $admin_netrc \
    -H 'Content-Type: application/json' \
    -XDELETE "$es_host/_security/user/$username?pretty"
}

password()
{
  curl -k --netrc-file $admin_netrc \
    -H 'Content-Type: application/json' \
    -XPOST "$es_host/_security/user/$username/_password?pretty" --data @- << EOS
{
  "password" : "$password"
}
EOS
}

version() {
  curl -k --netrc-file $user_netrc $es_host?pretty
}

indices() {
  curl -k --netrc-file $user_netrc "$es_host/_cat/indices?v"
}

tables() {
  indices
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

if [ -z "$username" ]; then
  echo "no username option"
  ret=`expr $ret + 1`
fi

if [ $ret -ne 0 ]; then
  exit $ret
fi

delete


#for arg in $args ; do
#  num=`LANG=C type $arg | grep 'function' | wc -l`
#
#  if [ $num -ne 0 ]; then
#    $arg
#  else
#    echo "no such function, $arg"
#    exit 1
#  fi
#done


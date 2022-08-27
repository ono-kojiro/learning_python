#!/bin/sh

set -e

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

es_host="https://192.168.0.98:9200/"

help() {
  cat - << EOS
usage : $0 -u <username> [-p <password>]
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
  echo "DEBUG : username is $username"
  echo "DEBUG : password is $password"
  curl -k -u $username:$password $es_host
}

ret=0

args=""

username=""
password=""

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

if [ -z "$password" ]; then
  echo -n "Password: "
  #read -p "Password: " -s password
  stty_orig=$(stty -g)
  stty -echo
  read password
  stty $stty_orig
fi


tty -s && echo

version


#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

flags=""
  
. ./apikey.bashrc
opnsense_host="localhost"
opnsense_port="8443"

base_url="https://${opnsense_host}:${opnsense_port}"

help()
{
  usage
}

usage()
{
  cat << EOS
usage : $0 [options] target1 target2 ...

  target:
    pytest
EOS

}

all()
{
  :
}

prepare()
{
  python3 -m pip install -r requirements.txt
}

test()
{
  pytest
}

args=""
while [ "$#" -ne 0 ]; do
  case $1 in
    -h )
      usage
      exit 1
      ;;
    -v )
      verbose=1
      ;;
    -* )
      flags="$flags $1"
      ;;
    * )
      args="$args $1"
      ;;
  esac
  
  shift
done

if [ -z "$args" ]; then
  help
  exit 1
fi

for target in $args; do
  target=`echo $target | tr '-' '_'`
  num=`LANG=C type $target 2>&1 | grep 'function' | wc -l`
  if [ "$num" -ne 0 ]; then
    $target
  else
    #echo "ERROR : $target is not shell function"
    #exit 1
    default $target
  fi
done


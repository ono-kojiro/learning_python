#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

flags=""
  
if [ -f ./myenv/bin/activate ]; then
  . ./myenv/bin/activate
fi
  
. ./apikey.shrc
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
    prepare
    init

    fetch
    extract

    lower
    spec
    api

    pytest

    mclean
EOS

}

all()
{
  :
}

prepare()
{
  sudo apt -y install python3-pip python3-venv
}

init()
{
  if [ ! -d myenv ]; then
    python3 -m venv myenv
  fi

  . ./myenv/bin/activate
  python3 -m pip install -r requirements.txt
}

fetch()
{
  mkdir -p work/archive/
  ssh firewall -l root \
    tar -C /usr/local/opnsense/mvc/app/controllers \
      -cJf /tmp/OPNsense.tar.xz OPNsense
  scp root@firewall:/tmp/OPNsense.tar.xz ./work/archive/
  ssh firewall -l root rm -f /tmp/OPNsense.tar.xz
}

extract()
{
  mkdir -p work/original
  cd work/original
  tar -xJvf ../archive/OPNsense.tar.xz
  cd ${top_dir}
}

lower()
{
  cd work
  srcdir="original"
  dstdir="source"

  rm -rf $dstdir
  mkdir -p $dstdir

  cd $srcdir

  find . -depth -path "*/Api/*Controller.php" | while read filepath; do
    lower=`echo "$filepath" | tr '[:upper:]' '[:lower:]'`
    echo "INFO: filepath is $filepath"
    
    dstpath="../$dstdir/$lower"
    mkdir -p `dirname $dstpath`
    cp -f "$filepath" "../$dstdir/$lower"
  done

  cd ${top_dir}
}

spec()
{
  cd work

  rm -rf specs
  mkdir -p specs

  {
     echo "CONTROLLERS_PHP = \\" 
     find ./source/opnsense/ -name "*controller.php" \
        | sed 's/\(.*\)/  \1 \\/'
     echo ""

  } > controllers.mk

  make -f ${top_dir}/generate_spec.mk

  cd ${top_dir}
}

api()
{
  cd work
  rm -rf api
  make -f ${top_dir}/generate_api.mk
  cd ${top_dir}
}

test()
{
  cp -f apikey.shrc .env
  PYTHONPATH=`pwd`/work/api/opnsense/core/api python3 example.py | jq .
}

install()
{
  python3 -m pip install -e .
}

mclean()
{
  rm -f ./work/OPNsense.tar.xz
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


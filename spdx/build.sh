#!/usr/bin/env sh

top_dir="$(cd "$(dirname "$0")" > /dev/null 2>&1 && pwd)"
cd $top_dir

spdx_examples_url="https://github.com/spdx/spdx-examples.git"

help()
{
  cat - << EOS
usage : $0 [target]
EOS

}

prepare()
{
  if [ ! -e "spdx-examples" ]; then
    git clone ${spdx_examples_url}
  else
    echo skip git clone
  fi  
}

clean()
{
  :
}

mclean()
{
  :
}

check()
{
  find ./spdx-examples -name "*.spdx" -print -exec ./example.py {} \;
}

all()
{
  :
}

args=""
while [ $# -ne 0 ]; do
  case $1 in
    -h )
      usage
      exit 1
      ;;
    -v )
      verbose=1
      ;;
    * )
      args="$args $1"
      ;;
  esac
  
  shift
done

if [ -z "$args" ]; then
  all
fi

for arg in $args; do
  num=`LANG=C type $arg | grep 'function' | wc -l`

  if [ $num -ne 0 ]; then
    $arg
  else
    echo "ERROR : $arg is not shell function"
    exit 1
  fi
done


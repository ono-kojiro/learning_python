#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

project="myproject"
app="myapp"

pwd

help()
{
  usage
}

usage()
{
  cat - << EOS
usage : $0 [options] target1 target2 ...

  target
    startproject
    startapp
    patch

    runserver

    all
EOS
}

all()
{
  startproject
  startapp
  patch

  runserver
}

startproject()
{
  django-admin startproject $project
}

startapp()
{
  cd $project
  python manage.py startapp $app
  python manage.py startapp accounts
  cd $top_dir
}

patch()
{
  cd $project
  #command patch -p0 -i ../0001-change_timezone.patch
  find ../patches/ -maxdepth 1 -name "*.patch" -print -exec /usr/bin/patch -p0 -i {} \;
  cd $top_dir
}


runserver()
{
  cd $project
  python manage.py runserver
  cd $top_dir
}

mclean()
{
  rm -rf $project
}


if [ $# -eq 0 ]; then
  usage
  exit 1
fi

args=""

while [ $# -ne 0 ]; do
  case "$1" in
    -h )
      usage
	  ;;
    -v )
      verbose=1
	  ;;
    *)
	  args="$args $1"
	  ;;
  esac

  shift

done

for target in $args ; do
  LANG=C type $target | grep function > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    $target
  else
    echo "$target is not a shell function"
  fi
done


#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

project="myproject"
appname="myapp"

prepare()
{
  python3 -m venv myenv
  . myenv/bin/activate
  python3 -m pip install -r requirements.txt
  python3 -m pip install --upgrade pip
}

if [ ! -e "myenv/bin/activate" ]; then
  prepare
fi

. ./myenv/bin/activate

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

    runserver
EOS
}

all()
{
  echo "INFO: create project"
  startproject
  echo "INFO: create app"
  startapp
  
  echo "INFO: add_apps"
  add_apps

  add_tests
}

startproject()
{
  if [ ! -d "$project" ]; then
    django-admin startproject $project
  fi
}

startapp()
{
  cd $project
  if [ ! -d "$appname" ]; then
    python manage.py startapp $appname
  fi
  cd $top_dir
}

add_apps()
{
  cd $project
  settings_py="$project/settings.py"

  apps=""
  apps="$apps $appname"
  apps="$apps django_extensions"
  apps="$apps rest_framework"

  for app in $apps; do
    cat $settings_py | grep "'${app}'"
    if [ "$?" -ne 0 ]; then
      sed -i -e "/INSTALLED_APPS = \[/a \ \ \ \ '${app}'," $settings_py
    fi
  done

  cd $top_dir
}

add_tests()
{
  cd $project
  rm -f $appname/tests.py
  mkdir -p $appname/tests

  touch $appname/tests/__init__.py
  
  cp -f $top_dir/test_simple.py $appname/tests/

  cd $top_dir
}

test()
{
  cd $project
  python manage.py test
  cd $top_dir
}

mclean()
{
  rm -rf $project
  rm -rf myenv
  #git clean -fdx -e "*.crt" -e "*.key" -e "*.pem"
}

if [ "$#" -eq 0 ]; then
  usage
  exit 1
fi

args=""

while [ "$#" -ne 0 ]; do
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


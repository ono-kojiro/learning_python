#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

project="assetmanager"
appname="assetmanager"

. ./.env

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

    install_apps
    allowed_hosts

    migrate
    runserver

    all
EOS
}

all()
{
  echo "INFO: create project"
  startproject
  echo "INFO: create app"
  startapp
  
  install_apps

  echo "INFO: mod"
  mod
  echo "INFO: migrate"
  migrate
  echo "INFO: mod2"
  mod2
  echo "INFO: allowed_hosts"
  allowed_hosts

  echo "INFO: mod4"
  mod4
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

debug()
{
  settings_py="${project}/${project}/settings.py"
  python3 extract_block.py $settings_py > installed_apps.yml
}

install_apps()
{
  echo "INFO: install_apps"
  cd ${project}
  settings_py="${project}/settings.py"
  line="django.contrib.staticfiles"

  apps=""
  apps="$apps $appname"
  apps="$apps django_extensions"
  apps="$apps rest_framework"

  for app in $apps; do
    cat $settings_py | grep "'${app}'"
    if [ "$?" -ne 0 ]; then
      sed -i -e "/'${line}',/a \ \ \ \ '${app}'," $settings_py
    fi
  done
}

rename_db()
{
  cd $project
  settings_py="asset_manager/settings.py"

  sed -i -e "s|'NAME': BASE_DIR / 'db.sqlite3',|'NAME': BASE_DIR / 'test_db.sqlite3',|" $settings_py

  cd $top_dir
}

migrate()
{
  cd $project
  rm -f db.sqlite3

  python3 manage.py makemigrations
  python3 manage.py migrate

  set -a
  . ${top_dir}/.env
  python3 manage.py createsuperuser --noinput
  set +a

  cd $top_dir
}

allowed_hosts()
{
  cd $project
  settings_py="${project}/settings.py"
  sed -i -e 's/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = \["\*"\]/' $settings_py
  cd $top_dir
}

runserver()
{
  cd $project
  python3 manage.py runserver ${SERVER_ADDR_PORT}
  cd $top_dir
}

runserver_plus()
{
  cd $project
  python manage.py runserver_plus --cert-file ${CERTFILE} ${SERVER_ADDR_PORT}
  cd $top_dir
}

run()
{
  runserver_plus
}

start()
{
  cd $project
  nohup python manage.py runserver_plus \
    --cert-file ${CERTFILE} ${SERVER_ADDR_PORT} &
  cd $top_dir
}

stop()
{
  cd $project
  pkill -f 'python manage.py runserver_plus'
  cd $top_dir
}

mclean()
{
  rm -rf $project
  rm -rf myenv
  #git clean -fdx -e "*.crt" -e "*.key"
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


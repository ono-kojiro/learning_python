#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

project="myproject"
application="myapp"

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
    startproject / project
    startapp / app

    init
    replace
    run

    migrate
    runserver

    all
EOS
}

all()
{
  startproject
  startapp

  init  
  replace
  
  allowed_hosts

  copy 

  update_init
  update_url
  migrate
  run
}

minimal()
{
  startproject
  startapp

  replace_installed_apps
  allowed_hosts
  migrate
  run
}

startproject()
{
  echo "INFO: create project"
  if [ ! -d "$project" ]; then
    django-admin startproject $project
  fi
}

project()
{
  startproject
}

startapp()
{
  echo "INFO: create app"
  cd $project
  if [ ! -d "$application" ]; then
    python manage.py startapp $application
  fi
  cd $top_dir
}

app()
{
  startapp
}

init()
{
  mkdir -p ${project}/${application}/admin/
  rm -f    ${project}/${application}/admin.py
  
  mkdir -p ${project}/${application}/models/
  rm    -f ${project}/${application}/models.py
  
  mkdir -p ${project}/${application}/views/
  rm    -f ${project}/${application}/views.py
}

replace()
{
  replace_installed_apps
  replace_url
}

replace_installed_apps()
{
  settings_py="${project}/${project}/settings.py"
  cp -f template/${project}/${project}/installed_apps.yml ${project}/${project}/
 
  cat ${settings_py} | grep -e '^import yaml$'
  if [ "$?" -ne 0 ]; then
    sed -i -e "/from pathlib import Path/a import yaml" $settings_py
  fi
  
  name='INSTALLED_APPS'
  python3 replace_list.py -n ${name} -p ${project} ${settings_py} > settings.py
  mv -f settings.py ${settings_py}
}

replace_url()
{
  cp -f template/${project}/urls.py \
     ${project}/${project}/

  cp -f template/${project}/urlpatterns.yml \
     ${project}/${project}/

  cp -f template/${application}/urls.py \
     ${project}/${application}/

}

copy()
{
  cp -r template/${project}/*     ${project}/${project}/
  cp -r template/${application}/* ${project}/${application}/
}

update_init()
{
  items="models views admin"
  for item in $items; do
    ./generate_init.py \
      -o ${project}/${application}/${item}/__init__.py \
      ${project}/${application}/${item}/
  done
}

update_url()
{
  app_dir="${project}/${application}"
  urls_py="${app_dir}/urls.py"
  echo "INFO: generate ${urls_py}"
  ./generate_urls.py -o ${urls_py} ${app_dir}/views/
  cat ${urls_py}
}

log()
{
  cat ${project}/nohup.out
}

migrate()
{
  echo "INFO: migrate"
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
  echo "INFO: allowed_hosts"
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

restart()
{
  stop
  start
}

mclean()
{
  rm -rf $project
  #rm -rf myenv
  #git clean -fdx -e "*.crt" -e "*.key"
}

test()
{
  pytest
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


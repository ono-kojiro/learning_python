#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

. ./.env

project="myproject"
application="myapp"

workdir="work"

prepare()
{
  python3 -m venv myenv
  . ./myenv/bin/activate
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

  replace
  allowed_hosts
  generate
  update_ini
  migrate
  run
}

startproject()
{
  echo "INFO: create project"
  if [ ! -d "${project}" ]; then
    django-admin startproject ${project} work
  fi
}

project()
{
  startproject
}

startapp()
{
  echo "INFO: create app"
  cd ${workdir}
  if [ ! -d "$application" ]; then
    python manage.py startapp $application
  fi
  cd $top_dir
}

app()
{
  startapp
}

create()
{
  startproject
  startapp
}

replace()
{
  replace_installed_apps
}

replace_installed_apps()
{
  settings_py="${workdir}/${project}/settings.py"
  cp -f template/project/installed_apps.yml ${workdir}/${project}/
 
  cat ${settings_py} | grep -e '^import yaml$'
  if [ "$?" -ne 0 ]; then
    sed -i -e "/from pathlib import Path/a import yaml" $settings_py
  fi
  
  name='INSTALLED_APPS'
  python3 replace_list.py -n ${name} -p ${project} ${settings_py} > settings.py
  mv -f settings.py ${settings_py}
}

log()
{
  cat ${project}/nohup.out
}

generate()
{
  components="models admin views serializers"

  for component in ${components}; do
    mkdir -p ${workdir}/${application}/${component}/
    rm -rf   ${workdir}/${application}/${component}.py
  done

  entities="device"
  for entity in ${entities}; do
    template="template/app/${entity}.yaml"

    python3 generate_model.py ${template} \
      > ${workdir}/${application}/models/${entity}_model.py
  
    python3 generate_admin.py ${template} \
      > ${workdir}/${application}/admin/${entity}_admin.py

    python3 generate_view.py ${template} \
      > ${workdir}/${application}/views/${entity}_view.py
  
    python3 generate_serializer.py \
      -o ${workdir}/${application}/serializers/${entity}_serializer.py \
      ${template}
  done

  templates=""
  for entity in ${entities}; do
    templates="${templates} template/app/${entity}.yaml"
  done

  python3 generate_url.py -o ${workdir}/${application}/urls_api.py \
     ${templates}

}

gen()
{
  generate
}

update_ini()
{
  cd ${workdir}/${application}/models
  {
    echo "# auo-generated"
    for f in *.py; do
      if [ "$f" = "__init__.py" ]; then
        continue
      fi

      class=`cat "$f" | grep -Eo 'class\s+\w+' | awk '{ print $2 }'`
      module=`echo "$f" | sed -e 's/\.py$//'`
      echo "from .${module} import ${class}"
    done
  } > __init__.py

  cd $top_dir
  
  
  cd ${workdir}/${application}/admin
  {
    echo "# auo-generated"
    for f in *_admin.py; do
      #class=`cat "$f" | grep -Eo 'register\(([^)]+)\)' \
      #        | sed -E 's/register\(([^)]+)\)/\1/'`
      module=`echo "$f" | sed -e 's/\.py$//'`
      #echo "from .${module} import ${class}Admin"
      echo "from . import ${module}"
    done
  } > __init__.py

  cd $top_dir
  
  cd ${workdir}/${application}/views
  {
    echo "# auo-generated"
    for f in *_view.py; do
      class=`cat "$f" | grep -Eo 'class\s+\w+' | awk '{ print $2 }'`
      module=`echo "$f" | sed -e 's/\.py$//'`
      echo "from .${module} import ${class}"
    done
  } > __init__.py

  cd $top_dir
  
  cd ${workdir}/${application}/serializers
  {
    echo "# auo-generated"
    for f in *_serializer.py; do
      class=`cat "$f" | grep -Eo '^class\s+\w+' | awk '{ print $2 }'`
      module=`echo "$f" | sed -e 's/\.py$//'`
      echo "from .${module} import ${class}"
    done
  } > __init__.py

  cd $top_dir
}

update_url()
{
  urls_py="${workdir}/${project}/urls.py"
    
  target="from django.urls import path, include"
  grep -q "$target" $urls_py || \
    sed -i "s/from django.urls import path/$target/" $urls_py

  grep -q "path('api/', include('myapp.urls_api'))" $urls_py || \
    sed -i "/^]/i\    path('api/', include('myapp.urls_api'))," $urls_py

}

migrate()
{
  echo "INFO: migrate"
  cd ${workdir}
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
  cd ${workdir}
  settings_py="${project}/settings.py"
  sed -i -e 's/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = \["\*"\]/' $settings_py
  cd $top_dir
}

runserver()
{
  cd ${workdir}
  python3 manage.py runserver ${SERVER_ADDR_PORT}
  cd $top_dir
}

runserver_plus()
{
  if [ ! -e "${CERTFILE}" ]; then
    cat ${SERVER_CRT} ${SERVER_KEY} > ${CERTFILE}
  fi
  cd ${workdir}
  python manage.py runserver_plus --cert-file ${CERTFILE} ${SERVER_ADDR_PORT}
  cd $top_dir
}

run()
{
  runserver_plus
}

start()
{
  cd ${workdir}
  rm -f nohup.out
  nohup python manage.py runserver_plus \
    --cert-file ${CERTFILE} ${SERVER_ADDR_PORT} &
  cd $top_dir
}

stop()
{
  cd ${workdir}
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
  rm -rf ${workdir}
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


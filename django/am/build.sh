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

  add_device
  device_admin

  add_view
  add_netif
  add_ipaddress

  update_init
  update_url
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
  
  cp -f template/${application}/admin/__init__.py \
    ${project}/${application}/admin/
 
  mkdir -p ${project}/${application}/models/
  rm    -f ${project}/${application}/models.py
  cp -f template/${application}/models/__init__.py \
    ${project}/${application}/models/
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

device_admin()
{
  init_py="myproject/myapp/admin/__init__.py"
  
  cp -f template/${application}/admin/device_admin.py \
    ${project}/${application}/admin/

  line="from .device_admin import DeviceAdmin"
  cat ${init_py} | grep -F "${line}"
  if [ "$?" -ne 0 ]; then
    echo "${line}" >> ${init_py}
  fi
}

copy()
{
  rm -f ${project}/${application}/models.py
  cp -r template/* ${project}/
}

device()
{
  rm -f    ${project}/${application}/models.py
  mkdir -p ${project}/${application}/models/
  cp -f template/myapp/models/device.py ${project}/${application}/models/

  init_py="${project}/${application}/models/__init__.py"
  touch ${init_py}

  line="from .device import Device"
  cat ${init_py} | grep -F "${line}"
  if [ "$?" -ne 0 ]; then
    echo "${line}" >> ${init_py}
  fi
}

add_device()
{
  device
}

add_view()
{
  mkdir -p ${project}/${application}/views/

  cp template/${application}/views/__init__.py \
    ${project}/${application}/views/

  cp template/${application}/views/device_api.py \
    ${project}/${application}/views/
}

update_init()
{
  items="models admin"
  for item in ${items}; do
    cd ${project}/${application}/${item}/
    rm -f __init__.py

    modules=`find *.py | grep -v '__init__'`
    for module in ${modules}; do
      echo "PYTHON: $module"
      class=`cat $module | grep -e '^class ' | \
        sed -E 's/class ([A-Za-z0-9_]*).*/\1/'`
      module=`basename $module .py`
      echo "CLASS: $class"
      echo "from .${module} import ${class}" >> __init__.py
    done

    cd ${top_dir}
  done

  items="views"
  for item in ${items}; do
    cd ${project}/${application}/${item}/
    rm -f __init__.py

    modules=`find *.py | grep -v '__init__'`
    for module in ${modules}; do
      echo "PYTHON: $module"
      funcs=`cat $module | grep -e '^def ' | \
        sed -E 's/def ([A-Za-z0-9_]*).*/\1/'`
      module=`basename $module .py`
      for func in $funcs; do
        echo "from .${module} import ${func}" >> __init__.py
      done
    done
    cd ${top_dir}
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

add_ipaddress()
{
  items="ipaddress macaddress"
  for item in $items; do
    cp -f template/myapp/models/${item}.py \
      ${project}/${application}/models/

    cp -f template/myapp/views/${item}_api.py \
      ${project}/${application}/views/

    cp -f template/myapp/admin/${item}_admin.py \
      ${project}/${application}/admin/
  done
}

add_netif()
{
  cp -f template/myapp/models/netif.py \
    ${project}/${application}/models/
  
  cp -f template/myapp/models/__init__.py \
    ${project}/${application}/models/
  
  cp -f template/myapp/views/netif_api.py \
    ${project}/${application}/views/
  cp -f template/myapp/views/__init__.py \
    ${project}/${application}/views/

  cp -f template/myapp/admin/netif_admin.py \
    ${project}/${application}/admin/

  cd ${project}/${application}/admin/
  rm -f __init__.py

  modules=`find *.py | grep -v '__init__'`
  for module in ${modules}; do
    echo "PYTHON: $module"
    class=`cat $module | grep -e '^class ' | \
      sed -E 's/class ([A-Za-z0-9_]*).*/\1/'`
    module=`basename $module .py`
    echo "CLASS: $class"
    echo "from .${module} import ${class}" >> __init__.py
  done

  cd ${top_dir}
}


log()
{
  cat ${project}/nohup.out
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


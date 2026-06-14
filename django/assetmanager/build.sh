#!/bin/sh

set -e

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

. ./.env

if [ ! -d myenv ]; then
  python3 -m venv myenv
fi

project="myproject"
application="myapp"

workdir="work"
  
Entities="Device NetIF IPv4 Manager Comment Remark"

entities=""
for Entity in ${Entities}; do
  entity=`echo $Entity | tr '[:upper:]' '[:lower:]'`
  entities="$entities $entity"
done

ref_yamls=""
for entity in ${entities}; do
  ref_yamls="${ref_yamls} template/app/${entity}_ref.yaml"
done

depend_yaml="${workdir}/depend.yaml"
category_yaml="${workdir}/category.yaml"
meta_yaml="${workdir}/meta.yaml"

prepare()
{
  #python3 -m venv myenv
  #. ./myenv/bin/activate
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

  cmp2ref
  category
  depend
  meta

  generate
  update_ini
  update_url
  migrate

  loaddata

  start
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

cmp2ref()
{
  for Entity in ${Entities}; do
    basename=`echo $Entity | tr '[:upper:]' '[:lower:]'`
    ./generators/cmp2ref.py \
      --output template/app/${basename}_ref.yaml \
      --name ${Entity} template/app/*_cmp.yaml
  done

  cat template/app/*_cmp.yaml > all_cmp.yaml
}

replace_installed_apps()
{
  echo "INFO: replace_installed_apps"
  settings_py="${workdir}/${project}/settings.py"
  cp -f template/project/installed_apps.yml ${workdir}/${project}/
 
  num=`cat ${settings_py} | grep -e '^import yaml$' | wc -l`
  if [ "$num" -eq 0 ]; then
    sed -i -e "/from pathlib import Path/a import yaml" $settings_py
  fi
  
  name='INSTALLED_APPS'
  ./replace_list.py -n ${name} -p ${project} ${settings_py} > settings.py
  mv -f settings.py ${settings_py}
}

log()
{
  cat ${project}/nohup.out
}

category()
{
   cmd="./generators/categorize_entity.py"
   cmd="$cmd -o ${category_yaml} template/app/*_ref.yaml"
   echo $cmd
   $cmd
   cat ${category_yaml}

   cat template/app/*_ref.yaml > all_ref.yaml
}

depend()
{
   cmd="./generators/generate_depend.py"
   cmd="$cmd -o ${depend_yaml} template/app/*_ref.yaml"
   echo $cmd
   $cmd
}

meta()
{
   cmd="./generators/generate_meta.py"
   cmd="$cmd -o ${meta_yaml} template/app/*_ref.yaml"
   echo $cmd
   $cmd
}

generate_model()
{
  for entity in ${entities}; do
    ref_yaml="template/app/${entity}_ref.yaml"

    echo "INFO: generate model for $entity"
    ./generators/generate_model.py \
      -d ${depend_yaml} \
      -l template/app \
      -o ${workdir}/${application}/models/${entity}_model.py \
      ${ref_yaml}
  done
}

generate_admin()
{
  for entity in ${entities}; do
    echo "INFO: generate admin for $entity"
    ./generators/generate_admin.py \
      -o ${workdir}/${application}/admin/${entity}_admin.py \
      -d ${depend_yaml} \
      -l template/app \
      template/app/${entity}_ref.yaml
  done
}

generate_view()
{
  for entity in ${entities}; do
    echo "INFO: generate view for $entity"
    ./generators/generate_view.py \
      -o ${workdir}/${application}/views/${entity}_view.py \
      -l template/app \
      -t viewset_template.j2 \
      template/app/${entity}_ref.yaml
  done
}

generate_serializer()
{
  for entity in ${entities}; do
    echo "INFO: generate serializer for $entity"
    ./generators/generate_serializer.py \
      -o ${workdir}/${application}/serializers/${entity}_serializer.py \
      -d ${depend_yaml} \
      -c ${category_yaml} \
      -l template/app \
      template/app/${entity}_ref.yaml
  done
}

generate_fixture()
{
  for entity in ${entities}; do
    echo "INFO: generate fixture for $entity"
    mkdir -p tests/data/
    ./generators/generate_fixture.py \
      -m ${meta_yaml} \
      -o tests/data/test_${entity}-fixtures.yaml \
      template/app/${entity}_ref.yaml
  done

  # debug
  # cat tests/data/test_*-fixtures.yaml > all-fixtures.yaml
}

generate_url()
{
  ./generators/generate_url.py -o ${workdir}/${application}/urls_api.py \
    -l template/app \
    -t urls_template.j2 \
     ${ref_yamls}
}

generate_admin_loader()
{
  ./generators/generate_admin_loader.py \
      -o ${workdir}/${application}/admin_loader.py \
      ${ref_yamls}
}

generate()
{
  components="models admin views serializers"

  for component in ${components}; do
    mkdir -p ${workdir}/${application}/${component}/
    rm -rf   ${workdir}/${application}/${component}.py
  done

  generate_model
  generate_admin

  generate_view

  generate_serializer

  generate_fixture

  generate_url

  generate_admin_loader

  echo "INFO: generate apps.py"
  ./generators/generate_apps.py \
    -n ${application} -o ${workdir}/${application}/apps.py

  rm -f ${workdir}/${application}/admin/__init__.py
}

gen()
{
  generate
}

update_ini()
{
  echo "INFO: generate models/__init__.py"

  ./generators/generate_ini.py \
    -o ${workdir}/${application}/models/__init__.py \
    template/app/*_ref.yaml

  echo "" > ${workdir}/${application}/admin/__init__.py
  echo "" > ${workdir}/${application}/views/__init__.py
  #echo "" > ${workdir}/${application}/serializers/__init__.py
  ./generators/generate_serializer_init.py \
    -o ${workdir}/${application}/serializers/__init__.py \
    template/app/*_ref.yaml
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

loaddata()
{
  echo "INFO: loaddata"
  models=`yq -r '.load_order[]' ${depend_yaml}`

  cd ${workdir}
  for model in ${models}; do
     m=`echo $model | tr '[:upper:]' '[:lower:]'`
     file="${top_dir}/tests/data/test_${m}-fixtures.yaml"
     echo "DEBUG: generate ${file} ..."
     #python3 manage.py loaddata ${file} --verbosity 3
     python3 manage.py loaddata ${file}
  done

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

generate_cert()
{
  if [ -z "${SERVER_CRT}" ]; then
    echo "ERROR: no SERVER_CRT variable" 1>&2
    exit 1
  fi
  
  if [ -z "${SERVER_KEY}" ]; then
    echo "ERROR: no SERVER_KEY variable" 1>&2
    exit 1
  fi
  
  if [ ! -f "${SERVER_CRT}" ]; then
    echo "ERROR: ${SERVER_CRT} not found" 1>&2
    exit 1
  fi
  
  if [ ! -f "${SERVER_KEY}" ]; then
    echo "ERROR: ${SERVER_KEY} not found" 1>&2
    exit 1
  fi
  
  rm -rf ${CERTFILE} 
  cat ${SERVER_CRT} ${SERVER_KEY} > ${CERTFILE}
  num=`wc -c < ${CERTFILE}`
  if [ "$num" -eq 0 ]; then
    echo "EEROR: empty certfile, ${CERTFILE}" 1>&2
    exit 1
  fi
}

runserver_plus()
{
  generate_cert

  cd ${workdir}
  python manage.py runserver_plus --cert-file ${CERTFILE} ${SERVER_ADDR_PORT}
  cd $top_dir
}

run()
{
  runserver_plus
}

shell()
{
  cd ${workdir}
  python manage.py shell
  cd $top_dir
}

start()
{
  generate_cert

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

generate_test()
{
  mkdir -p tests/data/
  for entity in ${entities}; do
    ./generators/generate_test.py -o tests/test_generated_${entity}.py \
      -m ${meta_yaml} \
      template/app/${entity}_ref.yaml
    cp -f template/app/${entity}_ref.yaml tests/data/
  done
}

test()
{
  generate_test
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


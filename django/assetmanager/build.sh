#!/bin/sh

set -e

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

. ./.env

project="myproject"
application="myapp"

workdir="work"
  
entities="Device NetIF IPv4 Manager Comment"
  
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

  cmp2ref
  category
  depend
  merge_models

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

  for entity in ${entities}; do
    basename=`echo $entity | tr '[:upper:]' '[:lower:]'`
    python3 cmp2ref.py --output template/app/${basename}_ref.yaml \
      --name ${entity} template/app/*_cmp.yaml
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
  python3 replace_list.py -n ${name} -p ${project} ${settings_py} > settings.py
  mv -f settings.py ${settings_py}
}

log()
{
  cat ${project}/nohup.out
}

category()
{
   cmd="python3 categorize_entity.py -o category.yaml template/app/*_ref.yaml"
   echo $cmd
   $cmd
   cat category.yaml

   cat template/app/*_ref.yaml > all_ref.yaml
}

depend()
{
   cmd="python3 generate_depend.py -o depend.yaml template/app/*_ref.yaml"
   echo $cmd
   $cmd
}

merge_models()
{
   all_models_yaml="all-models.yaml"
   model_yamls=`find ./template/app/ -name "*.yaml"`
   {
     for model_yaml in $model_yamls; do
       cat ${model_yaml}
     done

   } > ${all_models_yaml}
}

generate()
{
  components="models admin views serializers"

  for component in ${components}; do
    mkdir -p ${workdir}/${application}/${component}/
    rm -rf   ${workdir}/${application}/${component}.py
  done

  for entity in ${entities}; do
    entity=`echo $entity | tr '[:upper:]' '[:lower:]'`
    
    template="template/app/${entity}_ref.yaml"

    echo "INFO: generate model for $entity"
    python3 generate_model.py \
      -d depend.yaml \
      -o ${workdir}/${application}/models/${entity}_model.py \
      ${template}

    echo "INFO: generate admin for $entity"
    python3 generate_admin.py -d depend.yaml ${template} \
      > ${workdir}/${application}/admin/${entity}_admin.py

    echo "INFO: generate view for $entity"
    python3 generate_view.py ${template} \
      > ${workdir}/${application}/views/${entity}_view.py
  
    echo "INFO: generate serializer for $entity"
    python3 generate_serializer.py \
      -o ${workdir}/${application}/serializers/${entity}_serializer.py \
      -d depend.yaml \
      ${template}
    
    echo "INFO: generate fixture for $entity"
    mkdir -p tests/data/
    python3 generate_fixture.py \
      -o tests/data/test_${entity}-fixtures.yaml \
      ${template}
  done

  templates=""
  for entity in ${entities}; do
    entity=`echo $entity | tr '[:upper:]' '[:lower:]'`
    templates="${templates} template/app/${entity}_ref.yaml"
  done

  python3 generate_url.py -o ${workdir}/${application}/urls_api.py \
     ${templates}

  echo "INFO: generate admin loader"
  python3 generate_admin_loader.py \
      -o ${workdir}/${application}/admin_loader.py \
      ${templates}

  echo "INFO: generate apps.py"
  python3 generate_apps.py -n ${application} -o ${workdir}/${application}/apps.py

  rm -f ${workdir}/${application}/admin/__init__.py
}

gen()
{
  generate
}

update_ini()
{
  echo "INFO: generate models/__init__.py"

  python3 generate_ini.py \
    -o ${workdir}/${application}/models/__init__.py \
    template/app/*_ref.yaml

  echo "" > ${workdir}/${application}/admin/__init__.py
  echo "" > ${workdir}/${application}/views/__init__.py
  #echo "" > ${workdir}/${application}/serializers/__init__.py
  python3 generate_serializer_init.py \
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
  models=`yq -r '.load_order[]' depend.yaml`

  cd ${workdir}
  for model in ${models}; do
     m=`echo $model | tr '[:upper:]' '[:lower:]'`
     file="${top_dir}/tests/data/test_${m}-fixtures.yaml"
     echo "DEBUG: generate ${file} ..."
     python3 manage.py loaddata ${file} --verbosity 3
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


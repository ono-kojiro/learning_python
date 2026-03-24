#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

project="asset_manager"
appname="asset"

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
    patch

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
  
  echo "INFO: add"
  add

  echo "INFO: mod"
  mod
  echo "INFO: migrate"
  migrate
  echo "INFO: mod2"
  mod2
  echo "INFO: mod3"
  mod3

  echo "INFO: mod4"
  mod4
  echo "INFO: mod5"
  mod5
  echo "INFO: mod6"
  mod6
  echo "INFO: mod7"
  mod7
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

add_app()
{
  cd $project
  settings_py="asset_manager/settings.py"
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

add()
{
  add_app
}

mod()
{
  cd $project
  cp -f $top_dir/${appname}-models.py ${appname}/models.py
  cd $top_dir
}

migrate()
{
  cd $project
  rm -f db.sqlite3

  python3 manage.py makemigrations
  python3 manage.py migrate

  export DJANGO_SUPERUSER_USERNAME=admin
  export DJANGO_SUPERUSER_EMAIL=admin@example.com
  export DJANGO_SUPERUSER_PASSWORD=secret
  python3 manage.py createsuperuser --noinput
  cd $top_dir
}

mod2()
{
  cd $project
  cp -f $top_dir/${appname}-admin.py ${appname}/admin.py
  cd $top_dir
}

mod3()
{
  cd $project
  settings_py="asset_manager/settings.py"
  sed -i -e 's/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = \["\*"\]/' $settings_py
  cd $top_dir
}

mod4()
{
  cd $project
  cp -f $top_dir/asset-urls.py asset/urls.py
  urls_py="asset_manager/urls.py"

  sed -i -e "s|from django.urls import path$|from django.urls import path, include|" $urls_py
  sed -i -e "\|path('admin/', admin.site.urls),|a \ \ \ \ path('', include('asset.urls'))," $urls_py
  cd $top_dir
}

mod5()
{
  cd $project
  mkdir -p asset/templates/
  cp -f $top_dir/asset-views.py asset/views.py
  cp -f $top_dir/templates-index.html asset/templates/index.html
  cp -f $top_dir/templates-device_list.html asset/templates/device_list.html
  cp -f $top_dir/templates-device_add.html  asset/templates/device_add.html
  cd $top_dir
}

mod6()
{
  cd $project
  cp -f $top_dir/${appname}-serializers.py ${appname}/serializers.py
  cp -f $top_dir/${appname}-views_api.py   ${appname}/views_api.py
  cp -f $top_dir/${appname}-urls_api.py   ${appname}/urls_api.py
  
  urls_py="asset_manager/urls.py"
  sed -i -e "\|urlpatterns = \[|a \ \ \ \ path('api/', include('asset.urls_api'))," $urls_py
  cd $top_dir
}

mod7()
{
  cd $project
  rm -f ${appname}/tests.py
  mkdir -p ${appname}/tests/
  touch ${appname}/tests/__init__.py
  #cp -f $top_dir/test_unit_*.py ${appname}/tests/
  cd $top_dir
}

mod8()
{
  cd $project
  
  patchfile="$top_dir/100-enable_test_db_name.patch"
  patch -d ${project} -p0 --forward -i $patchfile
  
  patchfile="$top_dir/101-enable_logging.patch"
  patch -d ${project} -p0 --forward -i $patchfile

  cd $top_dir

}


runserver()
{
  cd $project
  python3 manage.py runserver 0.0.0.0:8000
  cd $top_dir
}

runserver_plus()
{
  cd $project
  python manage.py runserver_plus --cert-file $top_dir/luna2.pem 0.0.0.0:8000
  cd $top_dir
}

run()
{
  runserver_plus
}

clean()
{
  cd $project
  rm -f test_db.sqlite3
  rm -f db.sqlite3
  cd $top_dir
}

start()
{
  cd $project
  nohup python manage.py runserver_plus \
    --cert-file $top_dir/luna2.pem 0.0.0.0:8000 &
  cd $top_dir
}

test()
{
  #sh test-simple.sh
  cd $project
  cp -f $top_dir/test_unit_*.py ${appname}/tests/
  #python manage.py test --keepdb
  export TEST_DB_NAME="test_db.sqlite3"
  python manage.py test --keepdb -v 3 --debug-mode
  cd $top_dir
}

pytest()
{
  cd $project
  cp -f $top_dir/pytest.ini .
  cp -f $top_dir/test_integ_*.py .
  mkdir -p data/
  cp -f $top_dir/devices.yml data/
  cp -f $top_dir/nics.yml data/
  cp -f $top_dir/links.yml data/
  command pytest -v --reuse-db
  cd $top_dir
}

dbshell()
{
  cd $project
  python manage.py dbshell --database=default
  cd $top_dir
}

check()
{
  cd $project
  cp -f $top_dir/check_db.py .
  python3 check_db.py
  cd $top_dir
}


prove()
{
  command prove test-simple.sh
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
  git clean -fdx -e "*.crt" -e "*.key" -e "*.pem"
}


if [ $# -eq 0 ]; then
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


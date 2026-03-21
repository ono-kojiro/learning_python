#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

project="asset_manager"
app="asset"

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
  project
  app
  add

  mod
  migrate
  mod2
  mod3

  mod4
  mod5
}

startproject()
{
  django-admin startproject $project
}

project()
{
  startproject
}

startapp()
{
  cd $project
  python manage.py startapp $app
  cd $top_dir
}

app()
{
  startapp
}

add_app()
{
  cd $project
  settings_py="asset_manager/settings.py"
  sed -i -e "/'django.contrib.staticfiles',/a \ \ \ \ '$app'," $settings_py
  sed -i -e "/'django.contrib.staticfiles',/a \ \ \ \ 'django_extensions'," $settings_py
  cd $top_dir
}

add()
{
  add_app
}

mod()
{
  cd $project
  cp -f $top_dir/${app}-models.py ${app}/models.py
  cd $top_dir
}

migrate()
{
  cd $project
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
  cp -f $top_dir/${app}-admin.py ${app}/admin.py
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
  #sed -i -e "/'django.contrib.staticfiles',/a \ \ \ \ 'django_extensions'," $settings_py
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

runserver()
{
  cd $project
  python3 manage.py runserver 0.0.0.0:8000
  cd $top_dir
}

runssl()
{
  cd $project
  python manage.py runserver_plus --cert-file $top_dir/luna2.pem 0.0.0.0:8000
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


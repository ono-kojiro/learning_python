#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

project="asset_manager"
app="asset"

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

prepare()
{
  python3 -m venv myenv
  . myenv/bin/activate
  python3 -m pip install -r requirements.txt
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


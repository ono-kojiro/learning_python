#!/usr/bin/env sh

set -e
top_dir="$(cd "$(dirname "$0")" > /dev/null 2>&1 && pwd)"
cd $top_dir

#
# Add following 2 lines to /etc/postgresql/14/main/pg_hba.conf
#
# local   all   all                    ldap ldapserver=192.168.0.98  ldapprefix="uid=" ldapsuffix=",ou=Users,dc=example,dc=com"
#host    all   all     127.0.0.1/24   ldap ldapserver=192.168.0.98  ldapprefix="uid=" ldapsuffix=",ou=Users,dc=example,dc=com"

ret=0

database="sampledb"

help()
{
  cat - << EOS
usage: $0 <OPTIONS> <TARGET>
EOS
}

sysinstall()
{
  sudo apt-get -y install \
    postgresql-14 \
    postgresql-client-14 \
    postgresql-client-common \
    postgresql-common \
    libpq-dev
}

sysuninstall()
{
  sudo apt-get -y remove --purge \
    postgresql-14 \
    postgresql-client-14 \
    postgresql-client-common \
    postgresql-common \
    libpq-dev
}

pyinstall()
{
  python3 -m pip install psycopg2
}

start()
{
  sudo systemctl start postgresql
}

stop()
{
  sudo systemctl stop postgresql
}


status()
{
  sudo systemctl status 'postgresql*'
}

restart()
{
  sudo systemctl restart postgresql
}

is_active()
{
  sudo systemctl is-active postgresql
}

createdb()
{
  sudo -u postgres createdb $database
}

dropdb()
{
  sudo -u postgres dropdb $database
}

createuser()
{
  sudo -u postgres createuser --createdb $USER -w
}

dropuser()
{
  sudo -u postgres dropuser $USER
}

connect()
{
  psql $database -U $USER -W
}

databases()
{
  psql $database -U $USER -W -l
}


csr()
{
  mkdir -p $HOME/.postgresql
  csrfile=$HOME/.postgresql/postgresql.csr
  keyfile=$HOME/.postgresql/postgresql.key
  openssl req -new -nodes -text \
    -out $csrfile \
    -keyout $keyfile \
    -subj /CN=$USER

  echo output $csrfile and $keyfile
}

crt()
{
  csrfile=$HOME/.postgresql/postgresql.csr
  crtfile=$HOME/.postgresql/postgresql.crt
  servercrt=/etc/ssl/certs/server.crt
  serverkey=/etc/ssl/private/server.key

  primary_group=`id -gn $USER`

  sudo openssl x509 -req -text -days 3650 \
    -in $csrfile \
    -CA    $servercrt \
    -CAkey $serverkey \
    -CAcreateserial \
    -out $crtfile

  sudo chown $USER:$primary_group $crtfile
}

prepare()
{
  :
}

clean()
{
  dropuser
  dropdb
}

init()
{
  createuser
  createdb
}

all()
{
  python3 test.py
}


args=""

while [ $# -ne 0 ]; do
  case $1 in
    -h )
      help
      exit 1
      ;;
    -v )
      verbose=1
      ;;
    * )
      args="$args $1"
      ;;
  esac
  
  shift
done

if [ -z "$args" ]; then
  all
fi

for arg in $args; do
  num=`LANG=C type $arg | grep 'function' | wc -l`

  if [ $num -ne 0 ]; then
    $arg
  else
    echo "ERROR : $arg is not shell function"
    exit 1
  fi
done


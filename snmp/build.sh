#!/bin/sh

top_dir="$(cd "$(dirname "$0")" > /dev/null 2>&1 && pwd)"

# https://wiki.freebsd.org/KubilayKocak/SystemSecurityServicesDaemon

agent=192.168.10.1
logfile="snmp-${agent}.log"

walk()
{

  if [ ! -e "$logfile" ]; then
    snmpwalk \
      -v 2c \
      -c public \
      $agent \
      . \
      > snmp-${agent}.log
  fi

}

all()
{
  walk

  keyword="IP-MIB"
  cat $logfile | grep -e "^$keyword" > snmp-${keyword}.log
  #cat $logfile | grep -e "^$keyword" | sed -e 's/\..*//' | sort | uniq > snmp-${keyword}.log
}

test()
{
  keywords=`cat list.txt`
  for keyword in $keywords; do
    echo "DEBUG : $keyword"
    
  done
}

while [ $# -ne 0 ]; do
  case "$1" in
    -h | --help)
      usage
      exit 1
      ;;
    -o | --output)
      shift
      output=$1
      ;;
    *)
      break
      ;;
  esac

  shift
done

if [ $# -eq 0 ]; then
  all
fi

for target in "$@"; do
  num=`LANG=C type "$target" 2>&1 | grep 'function' | wc -l`
  if [ $num -eq 1 ]; then
    $target
  else
    echo "ERROR : $target is not a shell function"
  fi
done


#!/usr/bin/env sh

top_dir="$(cd "$(dirname "$0")" > /dev/null 2>&1 && pwd)"
cd $top_dir

if="vm-sw30"


all()
{
  arp
}

arp()
{
  host=`hostname`
  interface="$if"
  uname=`uname -a`
  logfile="arp_scan-${host}-${if}.arp"
  dt=`date "+%Y%m%d-%H%M%S"`
  machine_id=`cat /etc/machine-id`
  {
    echo "ARP_SCAN_BEGIN"
    echo "DATE: ${dt}"
    echo "HOSTNAME: ${host}"
    echo "MACHINE_ID: ${machine_id}"
    echo "UNAME: ${uname}"
    sudo arp-scan -l --interface ${interface}
    echo "ARP_SCAN_END"
  } | tee ${logfile}
}

args=""

while [ $# -ne 0 ]; do
  case $1 in
    -h )
      usage
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


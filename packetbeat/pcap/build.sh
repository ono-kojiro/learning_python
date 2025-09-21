#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

ret=0

analyze()
{
  pcapxzs=`find /var/lib/pcapd/ -type f -name "*.pcap.xz" | sort`

  for pcapxz in $pcapxzs; do
    outputdir=`basename -s .pcap.xz $pcapxz`
    pcapfile=`basename -s .xz $pcapxz`
    pcappath="$outputdir/$pcapfile"
  
    mkdir -p $outputdir
    echo "INFO: $pcapxz -> $pcappath"
    if [ ! -e "$pcappath" ]; then
      xz -dcf -k $pcapxz > $pcappath
    fi
    echo "INFO: $pcappath -> $outputdir"
    sh pcap2log.sh -i $pcappath -o $outputdir
    rm -f $pcappath
  done
}

help()
{
  usage
}

usage()
{
  cat << EOS
usage : $0 [options] -i input.pcap.xz -o outputdir
EOS

}

all()
{
  analyze
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
  #usage
  #exit 1
  args="analyze"
fi

for arg in $args; do
  num=`LANG=C type $arg 2>&1 | grep 'function' | wc -l`
  if [ $num -ne 0 ]; then
    $arg
  else
    #echo "ERROR : $arg is not shell function"
    #exit 1
    default $arg
  fi
done



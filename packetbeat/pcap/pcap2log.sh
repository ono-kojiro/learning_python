#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

ret=0
outputdir=""
pcappath=""

main()
{
  wd=$PWD
  mkdir -p $outputdir
  #cd $outputdir
  packetbeat \
      -c $top_dir/packetbeat.yml \
      -I $pcapfile \
      --path.data . \
      --path.config . \
      --path.data . \
      --path.logs $outputdir
  #cd $wd
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
  usage
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
    -i | --input )
      shift
      pcapfile="$1"
      ;;
    -o | --output-dir )
      shift
      outputdir="$1"
      ;;
    * )
      args="$args $1"
      ;;
  esac
  
  shift
done

#if [ -z "$args" ]; then
#  help
#  exit 1
#fi

if [ -z "$pcapfile" ]; then
  echo "ERROR: no input option"
  ret=`expr $ret + 1`
fi

if [ -z "$outputdir" ]; then
  echo "ERROR: no output-dir option"
  ret=`expr $ret + 1`
fi

if [ "$ret" -ne 0 ]; then
  exit $ret
fi

#for arg in $args; do
#  num=`LANG=C type $arg 2>&1 | grep 'function' | wc -l`
#  if [ $num -ne 0 ]; then
#    $arg
#  else
#    #echo "ERROR : $arg is not shell function"
#    #exit 1
#    default $arg
#  fi
#done

main


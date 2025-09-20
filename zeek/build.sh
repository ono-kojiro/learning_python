#!/bin/sh

# https://docs.zeek.org/en/master/log-formats.html
#
top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

workdir="work"

flags=""

help()
{
  usage
}

usage()
{
  cat << EOS
usage : $0 [OPTION...] [TARGET...]

target:
  deploy
EOS

}

all()
{
  #main
  :
}

prepare()
{
  python3 -m pip install -r requirements.txt
  
  sudo /opt/zeek/bin/zkg install logschema
}

schema()
{
  mkdir -p logschema
  cd logschema
  zeek logschema/export/jsonschema packages
  cd $top_dir
}

test()
{
  python3 verify.py
}

main()
{
  mkdir -p $workdir
  pattern="*.pcap.xz"
  pcapxzs=`find /var/lib/pcapd/ -type f -name "$pattern" | sort`
  for pcapxz in $pcapxzs; do
    echo $pcapxz
    basename=`basename -s .pcap.xz $pcapxz`
    outdir="$workdir/$basename"
    pcapfile="${basename}.pcap"
    pcappath="$outdir/${pcapfile}"

    mkdir -p $outdir

    echo "$pcapxz -> $pcappath"
    if [ ! -e "$pcappath" ]; then
      xz -dcf -k $pcapxz > $pcappath
    fi
    
    echo "analyze $pcapfile"
    cd $outdir
    ZEEK_LOG_SUFFIX=json zeek -C -r $pcapfile LogAscii::use_json=T
    rm -f $pcapfile
    cd $top_dir
  done
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
    -* )
      flags="$flags $1"
      ;;
    * )
      args="$args $1"
      ;;
  esac
  
  shift
done

if [ -z "$args" ]; then
  args="all"
fi

for arg in $args; do
  num=`LANG=C type $arg | grep 'function' | wc -l`
  if [ $num -ne 0 ]; then
    $arg
  else
    #echo "ERROR : $arg is not shell function"
    #exit 1
    default $arg
  fi
done


#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

timestamp=`LANG=C date "+%Y%m%d-%H%M%S"`

session=my-kernel-session
output_dir=/home/root/tmp
output_name=my-kernel-trace-$timestamp
output=$output_dir/$output_name

channel=mychannel

remote=yocto

dry_run=0


help()
{
  echo "usage : $0 [OPTIONS] target1 target2 ..."
}

execute_fio()
{
  cat - << 'EOS' | ssh -y $remote sh -s -- $dry_run
{
  dry_run=$1

  rws="read write"
  #rws="write"
  blocksizes="4k 8k 16k 32k 64k 128k 256k 512k"
  #blocksizes="16k"
  
  env="qemu_yocto"
  ioengine="sync"
  ramp_time="5s"
  runtime="20s"
  size="1G"
  format="normal"
      
  data_dir=/home/root/tmp/fio-data
  mkdir -p $data_dir

  log_dir=/home/root/tmp/fio-log
  mkdir -p $log_dir
  
  for rw in $rws ; do
    for bs in $blocksizes ; do
      title=$rw-$bs-$env
      filename=$data_dir/fio_data.bin
      logfile="$log_dir/${title}-${format}.json"

      cmd="/usr/bin/fio"
      cmd="$cmd --name=$title"
      cmd="$cmd --filename=$filename"
      cmd="$cmd --ioengine=$ioengine"
      cmd="$cmd --iodepth=1"
      cmd="$cmd --ramp_time=$ramp_time"
      cmd="$cmd --rw=$rw"
      cmd="$cmd --bs=$bs"
      cmd="$cmd --size=$size"
      cmd="$cmd --numjobs=1"
      cmd="$cmd --invalidate=1"
      cmd="$cmd --output-format=$format"
      cmd="$cmd --output $logfile"
      echo "  $cmd"
  
      if [ "$dry_run" != "0" ]; then
        EXEC=echo
      fi

      $EXEC $cmd
    done
  done

}
EOS

}

all()
{
  echo "This is all."
  session 
  #list
  channel
  event

  start

  echo "sleep 1sec ..."
  sleep 1
  echo "done."
  execute_fio

  stop
  destroy
  archive
  backup

}

session()
{
  cat - << 'EOS' | ssh -y $remote sh -s -- $session $output
  {
    session=$1
    output=$2

    # for kernel
    #   defaut num-subbuf : 4
    #   default subbuf-size : 1048576
    lttng create $session \
      --output=$output
  }
EOS

}

list()
{
  cat - << 'EOS' | ssh -y $remote sh -s -- $session $output
  {
    lttng list --kernel
    lttng list --kernel --syscall
  }
EOS

}

channel()
{
  cat - << 'EOS' | ssh -y $remote sh -s -- $session $channel
  {
    session=$1
    channel=$2

    lttng enable-channel \
      --kernel \
      --subbuf-size=4194304 \
      --num-subbuf=8 \
      --session=$session \
      $channel
  }
EOS

}

event()
{
  cat - << 'EOS' | ssh -y $remote sh -s -- $session $channel
  {
    session=$1
    channel=$2

    lttng enable-event \
      --kernel \
      --all \
      --session=$session \
      --channel=$channel

<< COMMENT
    lttng enable-event --kernel sched_switch,sched_process_fork
    lttng enable-event --kernel block_touch_buffer
    lttng enable-event --kernel block_dirty_buffer
    lttng enable-event --kernel block_rq_requeue
    lttng enable-event --kernel block_rq_complete
    lttng enable-event --kernel block_rq_insert
    lttng enable-event --kernel block_rq_issue
    lttng enable-event --kernel block_bio_bounce
    lttng enable-event --kernel block_bio_complete
    lttng enable-event --kernel block_bio_backmerge
    lttng enable-event --kernel block_bio_frontmerge
    lttng enable-event --kernel block_bio_queue
    lttng enable-event --kernel block_getrq
    lttng enable-event --kernel block_sleeprq
    lttng enable-event --kernel block_plug
    lttng enable-event --kernel block_unplug
    lttng enable-event --kernel block_split
    lttng enable-event --kernel block_bio_remap
    lttng enable-event --kernel block_rq_remap
    #lttng enable-event --kernel --syscall open,close
COMMENT

}
EOS

}

start()
{
  cat - << 'EOS' | ssh -y $remote sh -s -- $session $output
  {
    lttng start
  }
EOS

}

stop()
{
  cat - << 'EOS' | ssh -y $remote sh -s -- $session $output
  {
    lttng stop
  }
EOS

}

destroy()
{
  cat - << 'EOS' | ssh -y $remote sh -s -- $session $output
  {
    session=$1
    output=$2

    lttng destroy
  }
EOS

}

archive()
{
  cat - << 'EOS' | ssh -y $remote sh -s -- $session $output
  {
    session=$1
    output=$2

    basename=`basename $output`
    cd $output/..
    tar -C $output/.. -czvf $basename.tar.gz $basename
  }
EOS

}

backup()
{
  scp -q $remote:$output_dir/$output_name.tar.gz .
}

clean()
{
  echo "This is clean."
}

mclean()
{
  cat - << 'EOS' | ssh -y $remote sh -s -- $session $output
  {
    session=$1
    output=$2

    basename=`basename $output`
    cd $output/..
    rm -f $basename.tar.gz
    rm -rf $output
  }
EOS


}

args=""
extra_args=""

while [ "$#" != "0" ]; do
  case $1 in
    -h | --help)
      help
      exit 1
      ;;
    -v | --version)
      help
      exit 1
      ;;
    -n | --dry-run)
      dry_run=1
      ;;
    --)
      shift
      while [ "$#" != "0" ] ; do
        extra_args="$extra_args $1"
        shift
      done
      break
      ;;
    -*)
      echo "invalid arg, $1"
      exit 1
      ;;
    *)
      args="$args $1"
      ;;
  esac
  shift
done

if [ -z "$args" ]; then
  all
fi

for target in $args ; do
  type $target | grep function > /dev/null 2>&1
  res=$?
  if [ "$res" = "0" ]; then
    $target $extra_args
  else
    echo invalid target, "$target"
  fi
done


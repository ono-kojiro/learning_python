#!/bin/sh

blocksizes=
blocksizes="$blocksizes 4K"
blocksizes="$blocksizes 8K"
blocksizes="$blocksizes 16K 32K"
blocksizes="$blocksizes 64K 128K 256K 512K"
blocksizes="$blocksizes 1M 2M 4M 8M"
#blocksizes="$blocksizes 16M 32M"
#blocksizes="$blocksizes 64M 128M 256M 512M"

#rws="read"
rws="read write randread randwrite"

format="json"

#envs="native qemu_yocto kvm_ubuntu"
envs="native kvm_ubuntu"
format="json"
tm_str=`LANG=C date +%Y%m%d-%H%M%S`
log_dir=/tmp/fio-log

for rw in $rws ; do
  for bs in $blocksizes ; do
    for env in $envs ; do
      title=$rw-$bs-$env
      logfile="$log_dir/${title}-${format}.json"

      cat - << 'EOS' | ssh -y $env sh -s -- \
        $rw $bs $env $format $log_dir $title $logfile
{
  rw=$1
  bs=$2
  env=$3
  format=$4
  log_dir=$5
  title=$6
  logfile=$7

  ioengine=sync
  size=1G
  ramp_time=5s
  runtime=15s

  output_dir=/tmp/fio-data
  tmppath=$output_dir/fio_data-${rw}-${bs}.bin

  mkdir -p $output_dir
  mkdir -p $log_dir

  fio_version=`fio --version`
  echo "$env : $fio_version"

  cmd="/usr/bin/fio"

  cmd="$cmd --name=$title"
  cmd="$cmd --filename=$tmppath"
  cmd="$cmd --ioengine=$ioengine"
  cmd="$cmd --iodepth=1"
  cmd="$cmd --ramp_time=$ramp_time"
  cmd="$cmd --runtime=$runtime"
  cmd="$cmd --direct=1"
  cmd="$cmd --rw=$rw"
  cmd="$cmd --bs=$bs"
  cmd="$cmd --size=$size"
  cmd="$cmd --numjobs=1"
  cmd="$cmd --invalidate=1"
  cmd="$cmd --output-format=$format"
  cmd="$cmd --output $logfile"

  echo $cmd
  $cmd

  rm -f $tmppath
}

EOS
      mkdir -p ./log/$tm_str/
      scp $env:$logfile ./log/$tm_str/
    done


  done
done



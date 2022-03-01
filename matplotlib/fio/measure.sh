#!/bin/sh

blocksizes=
#blocksizes="$blocksizes 2K"
#blocksizes="$blocksizes 4K"
#blocksizes="$blocksizes 8K"
blocksizes="$blocksizes 16K 32K"
blocksizes="$blocksizes 64K 128K 256K 512K"
blocksizes="$blocksizes 1M 2M 4M 8M"
blocksizes="$blocksizes 16M 32M"
blocksizes="$blocksizes 64M"
#blocksizes="$blocksizes 64M 128M 256M 512M"

#rws="read"
rws="read write"
#rws="read write randread randwrite"

format="json"

envs="native"
#envs="qemu_yocto"
#envs="native qemu_yocto kvm_ubuntu"
#envs="native kvm_ubuntu"

tm_str=`LANG=C date +%Y%m%d-%H%M%S`
format="json"
runtime="10s"
size="20G"

logdir=/tmp/fio-log
numjobs=16

for rw in $rws ; do
  for bs in $blocksizes ; do
    for env in $envs ; do
  
      title=${env}-${rw}-${bs}
      logfile="${logdir}/${title}-${format}.json"

      cat - << 'EOS' | ssh -y -t $env sh -s -- \
        $rw $bs $env $logdir $logfile $title $format $runtime $size \
        $numjobs
{
  rw=$1; shift
  bs=$1; shift
  env=$1; shift
  logdir=$1; shift
  logfile=$1; shift
  title=$1; shift
  format=$1; shift
  runtime=$1; shift
  size=$1; shift
  numjobs=$1; shift

  ioengine=sync
  ramp_time=5s

  outdir=/tmp/fio-dat

      
  filename="${outdir}/${title}-${format}-${size}.bin"

  mkdir -p $logdir $outdir

  fio_version=`fio --version`

  dropcaches 3

  cmd="/usr/bin/fio"
  cmd="$cmd --name=$title"
  cmd="$cmd --filename=$filename"
  cmd="$cmd --ioengine=$ioengine"
  cmd="$cmd --iodepth=1"
  #cmd="$cmd --ramp_time=$ramp_time"
  cmd="$cmd --rw=$rw"
  cmd="$cmd --bs=$bs"
  cmd="$cmd --size=$size"
  cmd="$cmd --numjobs=$numjobs"
  cmd="$cmd --runtime=$runtime"
  cmd="$cmd --invalidate=1"
  cmd="$cmd --output-format=$format"
  cmd="$cmd --output=$logfile"

  echo $cmd
  $cmd

  rm -f $filename
}
EOS
      mkdir -p ./log/$tm_str/
      scp -q $env:$logfile ./log/$tm_str/
    done

  done
done



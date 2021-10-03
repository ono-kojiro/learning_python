#!/bin/sh

blocksizes=
blocksizes="$blocksizes 4K 8K"
blocksizes="$blocksizes 16K 32K"
blocksizes="$blocksizes 64K 128K 256K 512K"
#blocksizes="$blocksizes 1M 2M 4M 8M 16M 32M"
#blocksizes="$blocksizes 64M 128M 256M 512M"
#rws="read write randread randwrite"
rws="read write"

server=192.168.0.98
	
env="host"
ioengine=sync
size=4G
warmup_time=10
runtime=20

log_dir=./out

output_dir=/tmp/diskspd-test

mkdir -p $output_dir
mkdir -p $log_dir

for bs in $blocksizes; do
  for rw in $rws ; do

	title=$env-$rw-${bs}i
	tmppath=$output_dir/diskspd_data-${rw}-${bs}.bin

	write_percentage=0
		
	output="$log_dir/${title}.txt"

	if [ "$rw" = "read" ]; then
       write_percentage=0
	elif [ "$rw" = "write" ]; then
	   write_percentage=100
	else
	   echo "invalidate rw, $rw"
	   exit 1
	fi

	cmd="diskspd"
	cmd="$cmd --block-size=$bs"
	cmd="$cmd --create-files=$size"
	cmd="$cmd --duration=$runtime"
	cmd="$cmd --caching-options=d"
	cmd="$cmd --write=$write_percentage"
	cmd="$cmd --warmup-time=$warmup_time"
	cmd="$cmd --io-engine=k"
	cmd="$cmd $tmppath"

	echo $cmd
	echo $cmd           | ssh $server sh > $output
	echo rm -f $tmppath | ssh $server sh
  done
done


#!/bin/sh

blocksizes=
blocksizes="$blocksizes 4K 8K"
blocksizes="$blocksizes 16K 32K"
#blocksizes="$blocksizes 64K 128K 256K 512K"
#blocksizes="$blocksizes 1M 2M 4M 8M 16M 32M 64M 128M 256M 512M"
rws="read write randread randwrite"

formats="normal json"

mkdir -p out
server=192.168.0.98
	
env="host"
ioengine=sync
size=1G
ramp_time=2s
runtime=5s

for bs in $blocksizes; do
  for rw in $rws ; do

	title=$env-$rw-$bs
	tmppath=./fio_data-${rw}-${bs}.bin

	mkdir -p out

	cmd="/usr/local/bin/fio"
	cmd="$cmd --name=$title"
	cmd="$cmd --bandwidth-log"
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
	cmd="$cmd --status-interval=1s"
	#cmd="$cmd --eta=auto"

	for format in $formats ; do
		if [ "$format" = "json" ]; then
			ext="json"
		else
			ext="txt"
		fi

		output="out/${title}-${format}.${ext}"
		echo $output
		echo $cmd --output-format=$format --output $output | \
			ssh $server sh
		ssh $server cat $output > $output
    done
  done
done


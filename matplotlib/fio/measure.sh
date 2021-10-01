#!/bin/sh

env="host"

blocksizes="4K 8K 16K 32K 64K 128K 256K 512K"
#blocksizes="$blocksizes 1M 2M 4M 8M 16M 32M 64M 128M 256M 512M"
io_patterns="read write randread randwrite"
size=64M
ioengine=sync

ramp_time=2s
runtime=3s

mkdir -p out

for bs in $blocksizes; do
  for rw in $io_patterns; do
		title=$env-$rw-$bs
		output=out/$title.log
		tmppath=./fio_data-${rw}-${bs}.bin
		echo $title
		taskset -c 3 fio \
			--filename=$tmppath \
			--ioengine=$ioengine \
			--iodepth=1 \
			--ramp_time=$ramp_time \
			--runtime=$runtime \
			--direct=1 \
			--rw=$rw \
			--bs=$bs \
			--size=$size \
			--numjobs=1 \
			--invalidate=1 \
			--name=$title \
			--output-format=normal \
			--output $output 
		echo ""
		rm -f $tmppath

	done
done


#!/bin/sh

env="host"

blocksizes="4K 8K 16K 32K 64K 128K 256K 512K"
blocksizes="$blocksizes 1M 2M 4M 8M 16M 32M 64M 128M 256M 512M"
io_patterns="read write randread randwrite"
size=4G
ioengine=sync

for bs in $blocksizes; do
  for rw in $io_patterns; do
		title=$env-$rw-$bs
		output=$title.json
		tmppath=./fio_data-${rw}-${bs}.bin
		taskset -c 7 fio \
			--filename=$tmppath \
			--ioengine=$ioengine \
			--iodepth=1 \
			--ramp_time=3s \
			--direct=1 \
			--rw=$rw \
			--bs=$bs \
			--size=$size \
			--numjobs=1 \
			--invalidate=1 \
			--name=$title \
			--output-format=json \
			--output $output 

		rm -f $tmppath

	done
done


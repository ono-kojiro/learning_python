#!/bin/sh

env="host"

blocksizes="4k 8k 16k 32k 64k 128k 256k 512k"
io_patterns="read write"
tmppath=./fio_data.bin

for rw in $io_patterns; do
	for bs in $blocksizes; do
		title=$env-$rw-$bs
		output=$title.json
		echo $output
		rm -f $tmppath
		fio \
			-filename=$tmppath \
			-direct=1 \
			-rw=$rw \
			-bs=$bs \
			-size=2G \
			-numjobs=64 \
			-runtime=10 \
			-group_reporting \
			-name=$title \
			--output-format=json \
			--output $output
	done
done


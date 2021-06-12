#!/bin/sh

blocksizes="4k 8k 16k 32k"
io_patterns="read write"

for rw in $io_patterns; do
	for bs in $blocksizes; do
		title=$rw-$bs
		input=$title.json
		echo $input

	done
done


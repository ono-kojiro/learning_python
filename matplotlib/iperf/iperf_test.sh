#!/bin/sh

#env="host"
env="qemu"

buflens="4K 8K 16K 32K 64K 128K 256K 512K 1024K"

for buflen in $buflens; do
	logfile=$env-$buflen.json
	iperf3 -c 192.168.7.2 \
		--length $buflen \
		--get-server-output --json \
		> $logfile
done


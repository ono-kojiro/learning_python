#!/bin/sh

env="host"

num_threads="1 2 4"
server=192.168.0.98

for num_thread in $num_threads; do
	logfile=${server}-thread_${num_thread}.log
	ssh $server sysbench cpu --threads=$num_thread run > $logfile
done


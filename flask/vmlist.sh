#!/bin/sh
vms=`virsh list --all --name`
for vm in $vms; do
  virsh dumpxml $vm
done
#sudo vm list | python3 vmlist.py - > vmlist.json


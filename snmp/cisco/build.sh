#!/bin/sh

# write following lines in $HOME/.snmp/snmp.conf
#
#     mibdirs $HOME/.snmp/mibs
#     mibs    all
#

top_dir="$(cd "$(dirname "$0")" > /dev/null 2>&1 && pwd)"
cd $top_dir

agents="192.168.0.249"

dirlist="/usr/share/snmp/mibs"
dirlist="${dirlist}:/usr/share/snmp/librenms-mibs/nokia"
dirlist="${dirlist}:/usr/share/snmp/librenms-mibs/cisco"
dirlist="${dirlist}:/usr/share/snmp/cisco-mibs/v1"
dirlist="${dirlist}:/usr/share/snmp/cisco-mibs/v2"

comm="public"
flags=" -v 2c -c ${comm} -m ALL -M ${dirlist} -Cc -OX "

#oids=" \
#  SNMPv2-MIB::sysName \
#  IF-MIB::ifDescr \
#  IF-MIB::ifOutOctets \
#  IF-MIB::ifInOctets \
#  IF-MIB::ifTable \
#  RFC1213-MIB::ip \
#  IP-MIB::ipNetToMediaTable \
#  IP-MIB::ipNetToPhysicalPhysAddress \
#  IP-MIB::ipNetToPhysicalTable \
#  BRIDGE-MIB::dot1dTpFdbTable \
#"

oids=" \
  SNMPv2-MIB::sysName \
  SNMPv2-MIB::sysLocation \
  IF-MIB::ifIndex \
  IF-MIB::ifDescr \
  IF-MIB::ifType \
  IP-MIB::ipNetToMediaPhysAddress \
  BRIDGE-MIB::dot1dTpFdbPort \
"

help()
{
  cat - << EOF
usage : $0 <target>
EOF
}

snmp()
{
  for agent in ${agents}; do
    logfile="snmp-${agent}.log"
    errfile="snmp-${agent}.err"
    echo "INFO: $agent"
    {
      for oid in ${oids}; do
        snmpwalk ${flags} ${agent} ${oid}
      done
    } 2>${errfile} | tee ${logfile}
  done
}

json()
{
  for agent in ${agents}; do
    logfile="snmp-${agent}.log"
    jsonfile="snmp-${agent}.json"
    cmd="python3 snmp2json.py -o ${jsonfile} ${logfile}"
    echo $cmd
    $cmd
  done
}


if [ $# -eq 0 ]; then
  help
fi

for target in "$@"; do
  LANG=C type "$target" 2>&1 | grep 'function' > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    $target
  else
    default $target
  fi
done


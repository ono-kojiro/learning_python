#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"

mibs="ALL"
mibdirs="/usr/share/snmp/mibs"

flags="$flags -m $mibs"
flags="$flags -M $mibdirs"

echo "1..2"

exp="SNMPv2-MIB::sysName"
got=`snmptranslate $flags 1.3.6.1.2.1.1.5`

if [ "$exp" = "$got" ]; then
  echo ok
else
  echo not ok
fi

exp="SNMPv2-MIB::system"
got=`snmptranslate $flags 1.3.6.1.2.1.1`

if [ "$exp" = "$got" ]; then
  echo ok
else
  echo not ok
fi


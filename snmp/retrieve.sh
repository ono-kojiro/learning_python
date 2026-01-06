#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"

#oids="
#  SNMPv2-MIB::sysDescr
#  IF-MIB::ifDescr
#  IF-MIB::ifOutOctets
#  IF-MIB::ifInOctets
#  IF-MIB::ifTable
#  IF-MIB::interfaces
#  IP-MIB::ip
#  BRIDGE-MIB::dot1dTpFdbPort
#"

#
# BUFFALO:
#   BRIDGE-MIB::dot1dTpFdbPort,  MAC -> PortIndex
#
#oids="
#  SNMPv2-MIB::sysDescr
#  IF-MIB::ifTable
#  IP-MIB::ipNetToMediaPhysAddress
#  BRIDGE-MIB::dot1dTpFdbPort
#  LLDP-MIB::lldpRemSysName
#  BRIDGE-MIB::dot1dBridge
#"

# Default
oids="
  .
"

# SNMPv2-SMI::mib-2
#IP-MIB::ip
#BRIDGE-MIB::dot1dBridge

rm -f ${agent}.err

ret=0
agent=""
mibs=""
mibdirs=""
outfile=""
errfile=""

while [ "$#" -ne 0 ]; do
  case "$1" in
    -h | --help)
      usage
      exit 1
      ;;
    -e | --error)
      shift
      errfile=$1
      ;;
    -a | --agent)
      shift
      agent=$1
      ;;
    -m | --mibs)
      shift
      mibs=$1
      ;;
    -M | --mibdirs)
      shift
      mibdirs=$1
      ;;
    --oids)
      shift
      oids="$1"
      ;;
    -o | --output)
      shift
      outfile=$1
      ;;
    *)
      break
      ;;
  esac

  shift
done

if [ -z "$agent" ]; then
  echo "ERROR: no agent option" 1>&2
  ret=`expr $ret + 1`
fi

if [ -z "$outfile" ]; then
  echo "ERROR: no output option" 1>&2
  ret=`expr $ret + 1`
fi

if [ -z "$errfile" ]; then
  errfile="/dev/null"
fi

if [ -z "$mibs" ]; then
  mibs="ALL"
fi

if [ -z "$mibdirs" ]; then
  mibdirs="/usr/share/snmp/mibs"
fi

if [ "$ret" -ne 0 ]; then
  exit $ret
fi

# read agent config
if [ ! -e "${agent}.shrc" ]; then
  echo "ERROR: no config file, ${agent}.shrc"
  ret=`expr $ret + 1`
fi

if [ "$ret" -ne 0 ]; then
  exit $ret
fi

if [ -e "common.shrc" ]; then
  . ./common.shrc
fi

if [ -e "password.shrc" ]; then
  . ./password.shrc
fi

. ./${agent}.shrc

flags=""
flags="$flags -v $snmpver"

flags="$flags -l $seclevel"
flags="$flags -u $secname"
flags="$flags -a $authprotocol"
flags="$flags -A $authpassword"
flags="$flags -x $privprotocol"
flags="$flags -X $privpassword"

# Display table indexes in a more "program like" output
flags="$flags -OX"
#flags="$flags -Of"

flags="$flags -m $mibs"
flags="$flags -M $mibdirs"
flags="$flags -Pe"

{
  for oid in $oids; do
    cmd="snmpwalk $flags $agent $oid"
    echo "# CMD: $cmd"
    $cmd 2>>${errfile}
  done
} | tee ${outfile}


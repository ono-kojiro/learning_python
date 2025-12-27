#!/usr/bin/env python3

import sys
import re

import getopt
import yaml

from pprint import pprint
import json
from snmpjson import get_scalar_value, normalize_mac, get_ip_address
from snmpjson import get_dict_values, get_if2mac_table, get_mac2status_table
from snmpjson import  get_mac2addrs_table

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def read_json(jsonfile) :
    fp = open(jsonfile, mode='r', encoding='utf-8')
    data = json.load(fp)
    fp.close()
    return data

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
            [
                "help",
                "version",
                "output="
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    
    output = None
    
    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unknown option"
    
    if output is not None:
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(1)
  
    arpscan_data = read_json('arpscan.json')
    arp_mac2ip = arpscan_data['arp-scan']

    data = {}

    records = {}

    count = 0
    for filepath in args:
        #fp.write('DEBUG: {0}\n'.format(filepath))
        data = read_json(filepath)

        sysdescr = get_scalar_value(data, 'SNMPv2-MIB::sysDescr.0')
        selfmac  = get_scalar_value(data, 'BRIDGE-MIB::dot1dBaseBridgeAddress.0')
        selfmac = normalize_mac(selfmac)
        ipaddrs  = get_ip_address(data)

        if2status = get_dict_values(data, 'IF-MIB::ifOperStatus')
        if2descr  = get_dict_values(data, 'IF-MIB::ifDescr')
        if2type   = get_dict_values(data, 'IF-MIB::ifType')
        ifaces = get_dict_values(data, 'IF-MIB::ifIndex')
        if2macs = get_if2mac_table(data, 'BRIDGE-MIB::dot1dTpFdbPort')
        mac2status = get_mac2status_table(data, 'BRIDGE-MIB::dot1dTpFdbStatus')
        mac2addrs = get_mac2addrs_table(data)
    
        #print(ipaddrs)
        fp.write('{0}: {1}, {2}\n'.format(sysdescr, ipaddrs, selfmac))
        
        for iface in ifaces:
            status = if2status[iface]
            descr  = if2descr[iface]
            typ    = if2type[iface]
            
            if re.search(r'Ethernet', descr) and status == 'up(1)':
                fp.write('{0}: {1}, {2}, {3}\n'.format(iface, status, descr, typ))
                macs = if2macs[iface]
                for mac in macs:
                    fp.write('  -> {0}'.format(mac))
                    addrs = []
                    if mac in mac2addrs:
                        addrs = mac2addrs[mac]
                        for addr in addrs:
                            fp.write(', {0}(snmp)'.format(addr))
                    if mac in arp_mac2ip:
                        addr = arp_mac2ip[mac]['ip']
                        vndr = arp_mac2ip[mac]['vendor']
                        fp.write(', {0}(arp)'.format(addr))
                        fp.write(', {0}(arp)'.format(vndr))
                    if mac in mac2status :
                        status = mac2status[mac]
                        fp.write(', {0}(snmp)'.format(status))
                    fp.write('\n')
                    
        fp.write('\n')

    #yaml.dump(data,
    #    fp,
    #    allow_unicode=True,
    #    default_flow_style=False,
    #    sort_keys=True,
    #)

    #fp.write(
    #    json.dumps(
    #        data,
    #        indent=4,
    #        ensure_ascii=False,
    #        sort_keys=True,
    #    )
    #)
    fp.write('\n')

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()


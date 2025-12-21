#!/usr/bin/env python3

import sys
import re

import getopt
import yaml

from pprint import pprint
import json

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def read_json(jsonfile) :
    fp = open(jsonfile, mode='r', encoding='utf-8')
    data = json.load(fp)
    fp.close()
    return data

def get_mac2addrs_table(data) :
    mac2addrs = {}

    ip_mib = data.get('IP-MIB', None)
    if ip_mib :
       addrs = ip_mib.get('ipNetToMediaPhysAddress', None)
       if addrs :
           for tmp in addrs:
              items = addrs[tmp]
              for addr in items:
                  mac = items[addr]['val']
                  mac = normalize_mac(mac)

                  if not mac in mac2addrs :
                    mac2addrs[mac] = []
                  mac2addrs[mac].append(addr)

    return mac2addrs

def get_dict_values(data, oidname) :
    records = {}

    mibname, objname = re.split(r'::', oidname)

    res = data.get(mibname, None)
    if res is None:
        return records

    res = res.get(objname, None)
    if res is None:
        return records

    for key in res:
        item = res[key]
        val = item['val']
        records[key] = val

    return records

def get_scalar_value(data, oidname) :
    val = None

    mibname, objname = re.split(r'::', oidname)

    res = data.get(mibname, None)
    if res is None:
        return val

    res = res.get(objname, None)
    if res is None:
        return val

    return res['val']

def get_if2mac_table(data, oidname) :
    records = {}

    mibname, objname = re.split(r'::', oidname)

    res = data.get(mibname, None)
    if res is None:
        return records

    res = res.get(objname, None)
    if res is None:
        return records

    for mac in res:
        item = res[mac]
        iface = item['val']
        mac = re.sub(r'^STRING: ', '', mac)
        mac = normalize_mac(mac)
        if not iface in records:
            records[iface] = []

        records[iface].append(mac)

    return records

def normalize_mac(mac_str) :
    expr = r"([0-9a-f]{1,2})" + r"([-:]?([0-9a-f]{1,2}))" * 5 + r"$"
    m = re.match(expr, mac_str.lower())
    mac = ''

    if m :
        # 1, 3, 5, ... , 11
        for i in range(1, 12, 2) :
            val = int(m.group(i), 16)
            mac += ":{0:02x}".format(val)
        mac = re.sub(r'^:', '', mac)
        #print("DEBUG: {0} -> {1}".format(mac_str, mac))
    else :
        print("ERROR: invalid mac address, {0}".format(mac_str))
        sys.exit(1)

    return mac

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
        fp.write('{0}\n'.format(sysdescr))
        if2status = get_dict_values(data, 'IF-MIB::ifOperStatus')
        if2descr  = get_dict_values(data, 'IF-MIB::ifDescr')
        if2type   = get_dict_values(data, 'IF-MIB::ifType')
        ifaces = get_dict_values(data, 'IF-MIB::ifIndex')
        if2macs = get_if2mac_table(data, 'BRIDGE-MIB::dot1dTpFdbPort')
        mac2addrs = get_mac2addrs_table(data)
        
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


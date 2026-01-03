#!/usr/bin/env python3

import sys

import getopt
import json

import sqlite3

from snmpjson import get_scalar_value, normalize_mac, get_ip_address
from snmpjson import get_dict_values, get_if2mac_table, get_mac2status_table
from snmpjson import get_mac2addrs_table

from pprint import pprint

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def read_json(filepath) :
    with open(filepath, mode='r', encoding='utf-8') as fp :
        data = json.loads(fp.read())
        return data

def create_agents_table(conn, table):
    c = conn.cursor()

    sql = 'DROP TABLE IF EXISTS {0};'.format(table)
    c.execute(sql)

    sql = 'CREATE TABLE {0} ('.format(table)
    sql += 'id INTEGER PRIMARY KEY, '
    sql += 'ip TEXT, '
    sql += 'mac TEXT, '
    sql += 'sysdescr TEXT '
    sql += ');'

    c.execute(sql)

def create_interfaces_table(conn, table):
    c = conn.cursor()

    sql = 'DROP TABLE IF EXISTS {0};'.format(table)
    c.execute(sql)

    sql = 'CREATE TABLE {0} ('.format(table)
    sql += 'id INTEGER PRIMARY KEY, '
    sql += 'agent TEXT, '
    sql += 'idx TEXT, '
    sql += 'typ TEXT, '
    sql += 'status TEXT, '
    sql += 'descr TEXT '
    sql += ');'

    c.execute(sql)

def create_macaddrs_table(conn, table):
    c = conn.cursor()

    sql = 'DROP TABLE IF EXISTS {0};'.format(table)
    c.execute(sql)

    sql = 'CREATE TABLE {0} ('.format(table)
    sql += 'id INTEGER PRIMARY KEY, '
    sql += 'agent TEXT, '
    sql += 'idx TEXT, '
    sql += 'mac TEXT '
    sql += ');'

    c.execute(sql)

def create_macaddrs_view(conn, view):
    c = conn.cursor()

    sql = 'DROP VIEW IF EXISTS {0};'.format(view)
    c.execute(sql)

    sql = 'CREATE VIEW {0} AS '.format(view)
    sql += 'SELECT '
    sql += '  interfaces_table.agent AS agent, '
    sql += '  interfaces_table.idx AS idx, '
    sql += '  macaddrs_table.mac AS mac '
    sql += 'FROM interfaces_table '
    sql += 'LEFT OUTER JOIN macaddrs_table '
    sql += '  ON interfaces_table.idx = macaddrs_table.idx '
    sql += 'WHERE status = "up(1)" '
    sql += ';'

    c.execute(sql)


def insert_interface(conn, table, item):
    c = conn.cursor()
    sql = 'INSERT INTO {0} VALUES ( NULL, ?, ?, ?, ?, ?);'.format(table)
    lst = [
        item['agent'],
        item['idx'],
        item['typ'],
        item['status'],
        item['descr'],
    ]

    c.execute(sql, lst)

def insert_macaddr(conn, table, item):
    c = conn.cursor()
    sql = 'INSERT INTO {0} VALUES ( NULL, ?, ?, ?);'.format(table)
    lst = [
        item['agent'],
        item['idx'],
        item['mac'],
    ]

    c.execute(sql, lst)


def insert_agent(conn, table, item):
    c = conn.cursor()
    sql = 'INSERT INTO {0} VALUES ( NULL, ?, ?, ?);'.format(table)
    lst = [
        item['ip'],
        item['mac'],
        item['sysdescr'],
    ]
    c.execute(sql, lst)

def main():
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
	
    ret = 0

    if output is None :
        print("no output option", file=sys.stderr)
        ret += 1
	
    if ret != 0:
        sys.exit(1)

    conn = sqlite3.connect(output)
    create_agents_table(conn, 'agents_table')
    create_interfaces_table(conn, 'interfaces_table')
    create_macaddrs_table(conn, 'macaddrs_table')

    for jsonfile in args:
        data = read_json(jsonfile)

        sysdescr = get_scalar_value(data, 'SNMPv2-MIB::sysDescr.0')
        ips = get_ip_address(data)
        mac = get_scalar_value(data, 'BRIDGE-MIB::dot1dBaseBridgeAddress.0')
        mac = normalize_mac(mac)

        if len(ips) != 1 :
            print('WARNING: some IP address found', file=sys.stderr)
            print('WARNING: ips {0}'.format(ips))
            print('WARNING: use only {0}'.format(ips[0]))
            #sys.exit(1)
            
        ip = ips[0]

        item = {
            'sysdescr': sysdescr,
            'ip': ip,
            'mac': mac,
        }
        insert_agent(conn, 'agents_table', item)

        if2status = get_dict_values(data, 'IF-MIB::ifOperStatus')
        if2descr  = get_dict_values(data, 'IF-MIB::ifDescr')
        if2type   = get_dict_values(data, 'IF-MIB::ifType')
        ifaces = get_dict_values(data, 'IF-MIB::ifIndex')
        
        for iface in ifaces :
            status = if2status[iface]
            descr  = if2descr[iface]
            typ    = if2type[iface]

            item = {
                'agent': ip,
                'idx': iface,
                'typ' : typ,
                'status': status,
                'descr': descr,
            }
            insert_interface(conn, 'interfaces_table', item)
        
        if2macs = get_if2mac_table(data, 'BRIDGE-MIB::dot1dTpFdbPort')
        for iface in ifaces :
            if not iface in if2macs:
                continue

            macs = if2macs[iface]
            for mac in macs:
                item = {
                    'agent': ip,
                    'idx'  : iface,
                    'mac'  : mac,
                }
                insert_macaddr(conn, 'macaddrs_table', item)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()

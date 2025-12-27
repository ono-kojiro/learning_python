#!/usr/bin/env python3

import sys

import getopt
import json

import sqlite3

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def read_json(filepath) :
    with open(filepath, mode='r', encoding='utf-8') as fp :
        data = json.loads(fp.read())
        return data

def create_macaddrs_view(conn, view):
    c = conn.cursor()

    sql = 'DROP VIEW IF EXISTS {0};'.format(view)
    c.execute(sql)

    sql = 'CREATE VIEW {0} AS '.format(view)
    sql += 'SELECT '
    sql += '  interfaces_table.agent AS agent, '
    sql += '  interfaces_table.idx AS idx, '
    sql += '  macaddrs_table.mac AS mac, '
    sql += '  arp_table.ip AS ip '
    sql += 'FROM interfaces_table '
    sql += 'LEFT OUTER JOIN macaddrs_table '
    sql += '  ON interfaces_table.idx = macaddrs_table.idx '
    sql += 'LEFT OUTER JOIN arp_table '
    sql += '  ON macaddrs_table.mac = arp_table.mac '
    sql += 'WHERE status = "up(1)" '
    sql += ';'

    c.execute(sql)

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
    create_macaddrs_view(conn, 'macaddrs_view')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()

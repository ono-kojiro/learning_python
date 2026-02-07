#!/usr/bin/env python3

import sys

import getopt
import yaml

import sqlite3

from pprint import pprint

def read_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    docs = yaml.load_all(fp, Loader=yaml.loader.SafeLoader)

    items = []
    for doc in docs:
        for item in doc:
            items.append(item)

    fp.close()
    return items

def insert_asset(conn, item):
    table = 'assets_table'
    ph = ', ?' * 3
    sql = 'INSERT INTO {0} VALUES ( NULL{1} );'.format(table, ph)
    c = conn.cursor()
    record = [
        item['aid'],
        item['name'],
        item['descr'],
    ]
    c.execute(sql, record)
    
    table = 'interfaces_table'
    ph = ', ?' * 4
    sql = 'INSERT INTO {0} VALUES ( NULL{1});'.format(table, ph)
        
    aid = item['aid']

    for iface in item['interfaces']:
        ifid = iface['ifid']

        for prop in iface:
            if prop == 'ifid':
                continue

            val = iface[prop]

            record = [
                aid,
                ifid,
                prop,
                val,
            ]

            c.execute(sql, record)

def main() :
    ret = 0

    try:
        options, args = getopt.getopt(
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

    for option, arg in options:
        if option in ("-v", "-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = arg
        else:
            assert False, "unknown option"

    #if output is not None:
    #    fp = open(output, mode="w", encoding="utf-8")
    #else :
    #    fp = sys.stdout

    if output is None:
        print('ERROR: no output option')
        sys.exit(1)

    if ret != 0:
        sys.exit(1)

    conn = sqlite3.connect(output)

    for filepath in args :
        items = read_yaml(filepath)
        for item in items :
            aid = item['aid']
            descr = item['descr']

            insert_asset(conn, item)

    #print(data)

    #if output is not None:
    #    fp.close()

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()

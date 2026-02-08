#!/usr/bin/env python3

import sys

import getopt
import yaml

import sqlite3
from uuid import uuid4

from pprint import pprint

def read_list_from_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    docs = yaml.load_all(fp, Loader=yaml.loader.SafeLoader)

    items = []
    for doc in docs:
        for item in doc:
            items.append(item)

    fp.close()
    return items

def read_dict_from_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    docs = yaml.load_all(fp, Loader=yaml.loader.SafeLoader)

    items = {}
    for doc in docs:
        for item in doc:
            items[item] = doc[item]
    fp.close()
    return items

def insert_application(conn, asset_id, appl_id, item):
    table = 'applications_table'
    
    ph = ', ?' * 4
    sql = 'INSERT INTO {0} VALUES ( NULL{1});'.format(table, ph)
    c = conn.cursor()
        
    for prop in item:
        val = item[prop]

        record = [
            asset_id,
            appl_id,
            prop,
            val,
        ]
        c.execute(sql, record)

def insert_interface(conn, asset_id, iface_id, item):
    table = 'interfaces_table'
    c = conn.cursor()

    ph = ', ?' * 4
    sql = 'INSERT INTO {0} VALUES ( NULL{1});'.format(table, ph)
        
    for prop in item:
        val = item[prop]

        record = [
            asset_id,
            iface_id,
            prop,
            val,
        ]
        c.execute(sql, record)

def insert_asset(conn, table, uuid, prop, value):
    ph = ', ?' * 3
    sql = 'INSERT INTO {0} VALUES ( NULL{1} );'.format(table, ph)
    c = conn.cursor()
    params = [
        uuid,
        prop,
        value,
    ]
    c.execute(sql, params)

def insert_assets(conn, table, uuid, item):
    for prop in item:
        if prop in ('applications', 'interfaces') :
            continue

        val = item[prop]
        print('  {0}: {1}'.format(prop, val))
        record = {
            'uuid': uuid,
            'prop': prop,
            'value': val,
        }
        insert_asset(conn, table, uuid, prop, val)

def main() :
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
            [
              "help",
              "version",
              "output=",
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
        print('DEBUG: read {0}'.format(filepath))
        items = read_list_from_yaml(filepath)
        
        table = 'assets_table'
        for item in items :
            asset_id = str(uuid4())
            print('  asset_id: {0}'.format(asset_id))

            insert_assets(conn, table, asset_id, item)

            # insert 'interfaces'
            ifaces = item.get('interfaces', [])
            for iface in ifaces:
                iface_id = str(uuid4())
                insert_interface(conn, asset_id, iface_id, iface)

            appls = item.get('applications', [])
            for appl in appls:
                appl_id = str(uuid4())
                insert_application(conn, asset_id, appl_id, appl)

    #if output is not None:
    #    fp.close()

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()


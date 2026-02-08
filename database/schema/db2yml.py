#!/usr/bin/env python3

import sys

import getopt
import yaml

import sqlite3
from uuid import uuid4

from pprint import pprint

def get_applications(conn, asset_id):
    table = 'applications_table'

    sql = 'SELECT * FROM {0} '.format(table)
    sql += 'WHERE asset_id = ? '
    sql += 'ORDER BY id '
    sql += ';'

    params = [
        asset_id
    ]

    c = conn.cursor()
    rows = c.execute(sql, params)

    records = {}
    record = {}

    last_id = ''
    current_id = ''

    for row in rows :
        current_id = row['appl_id']
        prop = row['prop']
        value = row['value']

        if last_id != '' and last_id != current_id :
            records[last_id] = record
            record = {}

        record[prop] = value
        last_id = current_id
   
    if last_id != '' :
        records[last_id] = record
    return records    


def get_interfaces(conn, asset_id):
    table = 'interfaces_table'
    sql = 'SELECT * FROM interfaces_table '
    sql += 'WHERE asset_id = ? '
    sql += 'ORDER BY id '
    sql += ';'

    params = [
        asset_id
    ]

    c = conn.cursor()
    rows = c.execute(sql, params)

    records = {}
    record = {}

    last_iface_id = ''

    for row in rows :
        iface_id = row['iface_id']
        prop = row['prop']
        value = row['value']

        if last_iface_id != '' and last_iface_id != iface_id :
            records[last_iface_id] = record
            record = {}

        record[prop] = value
        last_iface_id = iface_id
   
    if last_iface_id != '' :
        records[last_iface_id] = record
    return records    

def get_assets(conn):
    table = 'assets_table'
    sql = 'SELECT * FROM assets_table '
    sql += 'ORDER BY id '
    sql += ';'

    c = conn.cursor()
    rows = c.execute(sql)

    last_asset_id = ''

    records = {}
    record = {}

    for row in rows:
        id = row['id']
        asset_id = row['asset_id']
        prop = row['prop']
        value = row['value']

        if last_asset_id != '' and last_asset_id != asset_id :
            records[last_asset_id] = record
            record = {}

        record[prop] = value
        last_asset_id = asset_id
   
    if last_asset_id != '' :
        records[last_asset_id] = record

    return records

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

    if output is not None:
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    #if output is None:
    #    print('ERROR: no output option')
    #    sys.exit(1)

    if ret != 0:
        sys.exit(1)


    for database in args :
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row    

        assets = get_assets(conn)

        for asset_id in assets:
            ifaces = get_interfaces(conn, asset_id)
            if ifaces:
                assets[asset_id]['interfaces'] = ifaces
        
            appls = get_applications(conn, asset_id)
            if appls:
                assets[asset_id]['applications'] = appls

    #pprint(assets)
    yaml.dump(assets, sys.stdout, allow_unicode=True)

    # text
    if output is not None:
        fp.close()

    # database
    #conn.commit()
    #conn.close()

if __name__ == "__main__":
    main()


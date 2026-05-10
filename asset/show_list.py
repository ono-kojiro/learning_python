#!/usr/bin/env python3

import sys

import getopt

import sqlite3

from pprint import pprint

def get_assets(conn) :
    sql = 'SELECT DISTINCT aid '
    sql += 'FROM assets_table '
    sql += 'ORDER BY aid '
    sql += ';'
    c = conn.cursor()

    rows = c.execute(sql)

    items = []
    for row in rows :
        aid = row['aid']
        items.append(aid)

    return items


def get_ifaces(conn, aid) :
    sql = 'SELECT aid, name, descr, ifid, prop, val '
    sql += 'FROM interfaces_view '
    sql += 'WHERE aid = ? '
    sql += 'ORDER BY aid, ifid, prop '
    sql += ';'
    c = conn.cursor()

    params = [
        aid,
    ]

    rows = c.execute(sql, params)

    records = []

    for row in rows :

        iface = {
            'aid': row['aid'],
            'ifid' : row['ifid'],
            'prop' : row['prop'],
            'val'  : row['val'],
            'descr' : row['descr'],
            'name' : row['name'],
        }
        records.append(iface)


def get_applications(conn, aid) :
    sql = 'SELECT aid, appid, prop, val '
    sql += 'FROM applications_table '
    sql += 'WHERE aid = ? '
    sql += 'ORDER BY aid, appid, prop '
    sql += ';'
    c = conn.cursor()

    params = [
        aid,
    ]

    rows = c.execute(sql, params)

    last_appid = ''

    records = []
    for row in rows :
        record = {
            'aid' : row['aid'],
            'appid': row['appid'],
            'prop': row['prop'],
            'val': row['val'],
        }

        records.append(record)

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

        aids = get_assets(conn)
        for aid in aids:
            print('AID: {0}'.format(aid))
            ifaces = get_ifaces(conn, aid)
            pprint(ifaces)
            apps = get_applications(conn, aid)
            pprint(apps)
        conn.close()

    if output is not None:
        fp.close()

    #conn.commit()
    #conn.close()

if __name__ == "__main__":
    main()

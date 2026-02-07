#!/usr/bin/env python3

import sys

import getopt

import sqlite3

from pprint import pprint

def show_assets(conn) :
    sql = 'SELECT aid, name, descr, ifid, prop, val '
    sql += 'FROM interfaces_view '
    sql += 'ORDER BY aid, ifid, prop '
    sql += ';'
    c = conn.cursor()

    rows = c.execute(sql)

    last_aid = ''
    last_ifid = ''

    for row in rows :
        aid = row['aid']
        ifid = row['ifid']
        prop = row['prop']
        val  = row['val']
        descr = row['descr']
        name = row['name']

        if last_aid != aid :
            if last_aid != '' :
                print('')

            print('---')
            print('- aid: {0}'.format(aid))
            print('  name: {0}'.format(name))
            print('  descr: {0}'.format(descr))
            print('')
            print('  interfaces:')
        
        if last_ifid != ifid :
            print('')
            print('  - ifid: {0}'.format(ifid))

        #print("{0} => {1}".format(prop, val))
        print('    {0}: {1}'.format(prop, val))

        last_aid = aid
        last_ifid = ifid

    print('')

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
        show_assets(conn)
        conn.close()

    if output is not None:
        fp.close()

    #conn.commit()
    #conn.close()

if __name__ == "__main__":
    main()

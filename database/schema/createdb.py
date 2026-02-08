#!/usr/bin/env python3

import sys

import getopt
import yaml

import sqlite3

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
        pprint(doc)
        for item in doc:
            pprint(item)
            items[item] = doc[item]

    fp.close()
    return items

def create_table(conn, table, columns) :

    sql = 'DROP TABLE IF EXISTS {0};'.format(table)
    c = conn.cursor()
    c.execute(sql)
    
    c = conn.cursor()
    sql = 'CREATE TABLE {0} ( '.format(table)
    sql += 'id INTEGER PRIMARY KEY'
    for column in columns:
        name = column['name']
        ctype = column['type']
        
        sql += ', {0} {1}'.format(name, ctype)
    sql += ');'

    c.execute(sql)

def create_ifaces_view(conn, view):
    sql = 'DROP VIEW IF EXISTS {0};'.format(view)
    c = conn.cursor()
    c.execute(sql)
    
    c = conn.cursor()
    sql = 'CREATE VIEW {0} AS '.format(view)
    sql += 'SELECT '
    sql += ' interfaces_table.*, assets_table.* '
    sql += 'FROM interfaces_table '
    sql += 'LEFT OUTER JOIN assets_table '
    sql += '  ON interfaces_table.aid = assets_table.aid '
    sql += 'ORDER BY aid, ifid '
    sql += ';'

    c.execute(sql)

def create_assets_view(conn, view) :
    sql = 'DROP VIEW IF EXISTS {0};'.format(view)
    c = conn.cursor()
    c.execute(sql)
    
    c = conn.cursor()
    sql = 'CREATE VIEW {0} AS '.format(view)
    sql += 'SELECT DISTINCT aid FROM interfaces_table '
    sql += 'GROUP BY ifid '
    sql += 'ORDER BY aid'
    sql += ';'
    c.execute(sql)

def create_views(conn) :
    create_assets_view(conn, 'assets_view')
    create_ifaces_view(conn, 'interfaces_view')

def main() :
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:c:",
            [
              "help",
              "version",
              "output=",
              "config=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None
    configfile = None

    for option, arg in options:
        if option in ("-v", "-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = arg
        elif option in ("-c", "--config"):
            configfile = arg
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
        #schema = read_list_from_yaml(filepath)
        schema = read_dict_from_yaml(filepath)
        for table in schema:
            columns = schema[table]
            print('{0}'.format(table))
            create_table(conn, table, columns)
            
    #create_views(conn)

    #if output is not None:
    #    fp.close()

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()

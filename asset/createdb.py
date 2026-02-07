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

def create_table(conn, config) :
    table = config['name']

    sql = 'DROP TABLE IF EXISTS {0};'.format(table)
    c = conn.cursor()
    c.execute(sql)
    
    c = conn.cursor()
    sql = 'CREATE TABLE {0} ( '.format(table)
    sql += 'id INTEGER PRIMARY KEY'
    for column in config['columns']:
        name = column['name']
        ctype = column['type']
        
        sql += ', {0} {1}'.format(name, ctype)
    sql += ');'

    c.execute(sql)

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
        configs = read_yaml(filepath)
        for config in configs:
            table = config['name']
            print('{0}'.format(table))
            create_table(conn, config)

    #if output is not None:
    #    fp.close()

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()

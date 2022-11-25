#!/usr/bin/python
# coding: utf-8

import sys

import getopt
import json

import sqlite3

import codecs

from pprint import pprint

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def read_json(filepath) :
    with open(filepath, mode='r', encoding='utf-8') as fp :
        data = json.loads(fp.read())
        return data

def create_table(conn, table):
    c = conn.cursor()

    sql = 'DROP TABLE IF EXISTS {0};'.format(table)
    c.execute(sql)

    sql = 'CREATE TABLE {0} ('.format(table)
    sql += 'id INTEGER PRIMARY KEY, '
    sql += 'name TEXT, '
    sql += 'val TEXT '
    sql += ');'

    c.execute(sql)

def insert_record(conn, table, record):
    c = conn.cursor()
    sql = 'INSERT INTO {0} VALUES ( NULL, ?, ?);'.format(table)
    list = [
        record['name'],
        record['val']
    ]

    c.execute(sql, list)

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

    if output == None :
        print("no output option")
        ret += 1
	
    if ret != 0:
        sys.exit(1)

    conn = sqlite3.connect(output)

    table = 'test_table'

    create_table(conn, table)

    for input in args:
        items = read_json(input)
        for item in items:
            name = item['name']
            val  = item['val']
            print(item)
            insert_record(conn, table, item)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()

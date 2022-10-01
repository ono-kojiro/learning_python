#!/usr/bin/python3

import sys

import getopt
import sqlite3

from pprint import pprint

def usage():
    print("Usage : {0}".format(sys.argv[0]))

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

def read_records(conn, table):
    c = conn.cursor()
    sql = 'SELECT * FROM {0};'.format(table)

    rows = c.execute(sql)
    for row in rows :
        name = row['name']
        val  = row['val']

        print('{0}, {1}'.format(name, val))

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

    for database in args :
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row

        table = 'test_table'
        read_records(conn, table)

    conn.close()

if __name__ == "__main__":
    main()

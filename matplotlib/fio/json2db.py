#!/usr/bin/python3

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
    sql += 'rw INTEGER, '
    sql += 'bs INTEGER, '
    sql += 'bw INTEGER '
    sql += ');'

    c.execute(sql)

def insert_record(conn, table, record):
    c = conn.cursor()
    sql = 'INSERT INTO {0} VALUES ( NULL, ?, ?, ?, ? );'.format(table)
    list = [ 
        record['name'],
        record['rw'],
        record['bs'],
        record['bw']
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

    table = 'fio_table'

    create_table(conn, table)

    rws = {
      'read' : 'read',
      'randread' : 'read',
      'write' : 'write',
      'randwrite' : 'write',
    }

    bss = {
      '1K' : 1024 * 1,
      '2K' : 1024 * 2,
      '4K' : 1024 * 4,
      '8K' : 1024 * 8,
      '16K' : 1024 * 16,
      '32K' : 1024 * 32,
      '64K' : 1024 * 64,
      '128K' : 1024 * 128,
      '256K' : 1024 * 256,
      '512K' : 1024 * 512,
    }

    for filepath in args:
        data = read_json(filepath)
        job = data['jobs'][0]

        job_options = job['job options']

        name = job_options['name']
        rw = job_options['rw']
        bs = job_options['bs']

        tmp = rws[rw]

        bw = job[tmp]['bw']

        if not bs in bss :
          print('error : no bs found, {0}'.format(bs))
          sys.exit(1)

        bs = bss[bs]

        print('{0}, {1}'.format(name, bw))
        record = {
            'name' : name,
            'rw'   : rw,
            'bs'   : bs,
            'bw'   : bw,
        }
        insert_record(conn, table, record)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()

#!/usr/bin/python3
import os
import re
import sys

import getopt
import json

import xml.etree.ElementTree as ET
import xmltodict

import sqlite3

from pprint import pprint

debug = False

def usage():
    print("Usage : {0} [OPTIONS] [FILE] [DIR] [DIR ...]".format(sys.argv[0]))

    msg = '''
find junit xmlfiles from directories, and concatenate them

  -o, --output             output junit xml string to file
  -x, --xsd XSDFILE        use xsdfile (default: ./junit-10.xsd)
'''

    print(msg)

def create_table(conn, table) :
    c = conn.cursor()
    
    sql = "DROP TABLE IF EXISTS {0};".format(table)
    c.execute(sql)

    sql = "CREATE TABLE {0} (".format(table)
    sql += "id INTEGER PRIMARY KEY, "
    sql += "name TEXT, "
    sql += "tests INTEGER, "
    sql += "failures INTEGER, "
    sql += "errors INTEGER "
    sql += ");"

    c.execute(sql)

def create_view(conn, view, table) :
    c = conn.cursor()

    sql = "DROP VIEW IF EXISTS {0};".format(view)
    c.execute(sql)

    sql = "CREATE VIEW {0} AS SELECT ".format(view)
    sql += "SUM(tests) AS sum_tests, "
    sql += "SUM(failures) AS sum_failures, "
    sql += "SUM(errors) AS sum_errors "
    sql += "FROM {0};".format(table)

    c.execute(sql)

def insert_record(conn, table, record) :
    c = conn.cursor()

    sql = "INSERT INTO {0} VALUES ( NULL, ?, ?, ?, ? );".format(table)

    data = [
        record["name"],
        record["tests"],
        record["failures"],
        record["errors"],
    ]

    c.execute(sql, data)

def read_lines(filepath) :
    fp = open(filepath, mode="r", encoding="utf-8")
    lines = ""

    is_testsuites = 0

    while 1:
        line = fp.readline()
        if not line :
            break

        line = re.sub(r'\r?\n?$', '', line)

        if is_testsuites == 0 :
            m = re.search(r'^<testsuites>', line)
            if m :
                is_testsuites = 1
        
        if is_testsuites :
            lines += line + '\n'
            
    fp.close()

    return lines

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
            [
                "help",
                "version",
                "output=",
            ],
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
        else :
            assert False, "unhandled option"

    if ret != 0:
        sys.exit(1)

    #if output is not None:
    #    fp = open(output, mode="w", encoding="utf8")
    #else:
    #    fp = sys.stdout

    if len(args) == 0 :
        usage()
        sys.exit(1)

    table = "results_table"
    view  = "summary_view"

    conn = sqlite3.connect(output)
    create_table(conn, table)
    create_view(conn, view, table)

    for filepath in args :
        lines = read_lines(filepath)
        root = ET.fromstring(lines)

        for ts in root.findall('./testsuite[@name]') :
            name = ts.attrib['name']

            data = xmltodict.parse(
                ET.tostring(ts)
            )

            tests    = int(data["testsuite"]["@tests"])
            failures = int(data["testsuite"]["@failures"])
            errors   = int(data["testsuite"]["@errors"])

            #print("{0}".format(name))
            #print("  tests    : {0}".format(tests))
            #print("  failures : {0}".format(failures))
            #print("  errors   : {0}".format(errors))

            insert_record(conn, table,
                {
                    "name" : name,
                    "tests" : tests,
                    "failures" : failures,
                    "errors" : errors,
                }
            )

    #if output is not None:
    #    fp.close()

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()


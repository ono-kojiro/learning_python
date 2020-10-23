#!/usr/bin/python3

import sys

import getopt
import json

import re

import xlrd

from pprint import pprint

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hvo:", ["help", "version", "output="])
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
	
    if output == None :
        print("no output option")
        ret += 1
	
    if ret != 0:
        sys.exit(1)
    

    fp = open(output, mode='w', encoding='utf-8')

    for filepath in args:
        print("arg : {0}".format(filepath))
        fp.write("# file : {0}\n".format(filepath))
        book = xlrd.open_workbook(filepath)

        pprint(book)
        for sheet in book.sheets() :
            fp.write("#   sheet : {0}\n".format(sheet.name))
            for row in range(sheet.nrows) :
                fp.write(" ")
                for col in range(sheet.ncols) :
                    cell = sheet.cell(row, col)
                    val  = cell.value
                    if col != 0 :
                        fp.write("\t")
                    fp.write("{0}".format(val))
                fp.write("\n")
	
    fp.close()
	
if __name__ == "__main__":
	main()

#!/usr/bin/python3

import sys

import getopt
import json

import re

import xlrd
from datetime import datetime

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
            fp.write("# sheet : {0}\n".format(sheet.name))
            for row in range(sheet.nrows) :
                fp.write(" ")
                for col in range(sheet.ncols) :
                    cell = sheet.cell(row, col)
                    type = cell.ctype
                    val  = cell.value
                    if type == xlrd.XL_CELL_EMPTY :
                        pass
                    elif type == xlrd.XL_CELL_TEXT :
                        pass
                    elif type == xlrd.XL_CELL_NUMBER :
                        if int(val) == val :
                            val = int(val)
                    elif type == xlrd.XL_CELL_DATE :
                        py_date = datetime(*xlrd.xldate_as_tuple(val, book.datemode))
                        val = py_date.strftime("%Y-%m-%d")

                        pass
                    elif type == xlrd.XL_CELL_BOOLEAN :
                        pass
                    elif type == xlrd.XL_CELL_ERROR :
                        pass
                    elif type == xlrd.XL_CELL_BLANK :
                        pass

                    if col != 0 :
                        fp.write("\t")
                    fp.write("{0}".format(val))
                fp.write("\n")
            fp.write("# enf of sheet : {0}\n".format(sheet.name))
        fp.write("# enf of file : {0}\n".format(filepath))
	
    fp.close()
	
if __name__ == "__main__":
	main()

#!/usr/bin/env python3

import os
import sys
import re

import getopt

import serial
import io

from pprint import pprint

def usage():
    print("Usage : {0} -b baudrate -p port".format(sys.argv[0]))

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvb:p:",
            [
                "help",
                "version",
                "baudrate=",
                "port=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
   
    baudrate = None
    port = None 
    
    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-b", "--baudrate"):
            baudrate = a
        elif o in ("-p", "--port"):
            port = a
        else:
            assert False, "unknown option"
    
    if port is None :
        print('ERROR : no port option')
        ret += 1

    if baudrate is None :
        print('ERROR : no baudrate option')
        ret += 1

    if ret != 0:
        sys.exit(1)

    #if len(args) == 0 :
    #    usage()
    #    sys.exit(1)
    
    #if output is not None :
    #    fp = open(output, mode='w', encoding='utf-8')
    #else :
    #    fp = sys.stdout

    ser = serial.Serial(port, baudrate, timeout=1);
    print(ser.name)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

    while True :
        line = sio.readline()
        print(line)

    sio.write("root\n")
    sio.flush()
    while True :
        line = sio.readline()
        print(line)

    ser.close()
    
if __name__ == "__main__":
    main()


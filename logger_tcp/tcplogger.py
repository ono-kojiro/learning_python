#!/usr/bin/env python3

import os
import sys

import getopt
import socket

import logging
from logging.handlers import SysLogHandler

def usage():
    msg = '''
usage: python3 tcplogger.py -h host -p port message
'''
    print(msg, file=sys.stderr)

def main():
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "vo:h:p:",
            [
              "help",
              "version",
              "output=",
              "host=",
              "port=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None
    host   = None
    port   = None

    for opt, arg in options:
        if opt in ("-v", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-h", "--host"):
            host = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        else:
            assert False, "unknown option"

    if output is not None:
        fp = open(output, mode='w', encoding='utf-8')
    else :
        fp = sys.stderr
   
    if host is None :
        print('ERROR: no host option', file=sys.stderr)
        ret += 1

    if port is None :
        print('ERROR: no port option', file=sys.stderr)
        ret += 1

    if ret :
        sys.exit(ret)
        
    hostname = socket.gethostname()
    appname  = sys.argv[0]
    process_id = os.getpid()

    for msg in args:
        # Example usage
        tmp  = "{0}".format(hostname)
        tmp += " {0}[{1}]:".format(appname, process_id)
        msg  = tmp + " " + msg

        print('host: {0}'.format(host))
        print('port: {0}'.format(port))
        print('msg : {0}'.format(msg))
        
        try :
            logger = logging.getLogger(appname)
            logger.setLevel(logging.INFO)
            
            handler = SysLogHandler(address=(host, port),
                socktype=socket.SOCK_STREAM)
            
            logger.addHandler(handler)
            logger.info(msg)
        except Exception as e:
            print("{0}".format(e), file=sys.stderr)

if __name__ == '__main__' :
    main()


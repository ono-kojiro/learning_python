#!/usr/bin/env python3

import os
import sys

import re

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
            "vo:h:p:P:",
            [
              "help",
              "version",
              "output=",
              "host=",
              "port=",
              "priority=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None
    host   = None
    port   = None
    priority = "local3.info"

    for opt, arg in options:
        if opt in ("-v", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-h", "--host"):
            host = arg
        elif opt in ("-P", "--priority"):
            priority = arg
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

    m = re.search(r'([^.]+)\.([^.]+)', priority)
    if not m :
        print('ERROR: invalid priority, {0}'.format(priority))
        sys.exit(1)

    facility = m.group(1)
    level    = m.group(2)
        
    hostname = socket.gethostname()
    process_id = os.getpid()
        
    print('priority: {0}'.format(priority))
    print('host: {0}'.format(host))
    print('port: {0}'.format(port))
    print('facility: {0}'.format(facility))
    print('level: {0}'.format(level))

    for msg in args:
        print('msg : {0}'.format(msg))
        
        try :
            logger = logging.getLogger(sys.argv[0])
            logger.setLevel(getattr(logging, level.upper(), logging.INFO))
            logger.setLevel(logging.INFO)

            handler = SysLogHandler(address=(host, port),
                socktype=socket.SOCK_STREAM)
            
            fmt = '{0} %(name)s[%(process)d]: %(message)s'.format(hostname)
            formatter = logging.Formatter(fmt)
            handler.setFormatter(formatter)
 
            logger.addHandler(handler)
            logger.info(msg)
        except Exception as e:
            print("{0}".format(e), file=sys.stderr)

if __name__ == '__main__' :
    main()


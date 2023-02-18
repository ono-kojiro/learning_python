#!/usr/bin/env python3

import sys
import getopt

import json
import psutil

from datetime import datetime, timedelta, timezone

def usage():
    print(f"Usage : {sys.argv[0]}")

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:i:n:",
            [
                "help",
                "version",
                "output=",
                "index=",
                "number=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None
    index  = None
    num    = 3

    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-i", "--index"):
            index = a
        elif o in ("-n", "--num"):
            num = int(a)
        else:
            assert False, "unknown option"
    
    tz = timezone(timedelta(hours=+0), 'UTC')
    now = datetime.now(tz)
    
    if index is None:
        #print('ERROR : no index option', file=sys.stderr)
        #ret += 1
        index = now.strftime('mymetrics-%Y.%m.%d')
    
    if ret != 0:
        sys.exit(1)

    if output is not None:
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    for i in range(num) :
        data = { "index" : { "_index" : index } }
        fp.write(json.dumps(data) + '\n')

        now = datetime.now(tz)
        ts = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        cpu = psutil.cpu_percent(interval=1)

        data = {
            "key" : i,
            "val" : i,
            "@timestamp" : ts,
            "cpu" : cpu,
        }
        fp.write(json.dumps(data) + '\n')

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

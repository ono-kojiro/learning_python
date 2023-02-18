#!/usr/bin/env python3

import sys
import getopt

import re
import json
import psutil

import time

from datetime import datetime, timedelta, timezone

import subprocess
import shlex

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
    num    = 1

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
        cmd = "free -m"
        tokens = shlex.split(cmd)
        res = subprocess.run(tokens, capture_output=True, text=True).stdout

        #       total  used   free shared buff/cache available
        # Mem:  15883 11665    301    510       3916      3366
        # Swap:  8191  2295   5896

        mem_percent = None

        lines = res.splitlines()
        for line in lines :
            #print(line)
            m = re.search(r'^Mem:\s+(\d+)\s+(\d+)', line)
            if m :
                total = int(m.group(1))
                used  = int(m.group(2))

                mem_percent = "{0:0.2f}".format(used * 100.0 / total)

        if mem_percent is None :
            print('ERROR : response of command "{0}" failed'.format(cmd))
            print(lines)
            continue

        data = { "index" : { "_index" : index } }
        fp.write(json.dumps(data) + '\n')

        now = datetime.now(tz)
        ts = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        #cpu = psutil.cpu_percent(interval=1)

        mem = 1
        data = {
            "@timestamp" : ts,
            "mem" : float(mem_percent),
        }
        fp.write(json.dumps(data) + '\n')

    #time.sleep(1)

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

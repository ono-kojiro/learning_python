#!/usr/bin/env python3

import sys
import re

import getopt

import json

STATE_INIT   = 0
STATE_HEADER = 1
STATE_RECORD = 2

def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")

def main():
    ret = 0

    try:
        options, args = getopt.getopt(
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
        sys.exit(1)

    output = None

    for option, optarg in options:
        if option == "-v":
            usage()
            sys.exit(1)
        elif option in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif option in ("-o", "--output"):
            output = optarg
        else:
            assert False, "unknown option"

    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(ret)

    config  = {}
    records = {}

    for filepath in args:
        fp_in = open(filepath, mode="r", encoding="utf-8")

        state = STATE_INIT

        while 1 :
            line = fp_in.readline()
            if not line :
                break

            line = re.sub(r'\r?\n?$', '', line)

            # change state
            if state == STATE_INIT :
                if line == 'ARP_SCAN_BEGIN':
                    state = STATE_HEADER
                pass
            elif state == STATE_HEADER :
                if re.search(r'^Starting arp-scan', line):
                    state = STATE_RECORD
                pass
            elif state == STATE_RECORD :
                if re.search(r'^ARP_SCAN_END', line):
                    state = STATE_RECORD
                pass
            
            # read value
            if state == STATE_INIT :
                pass
            elif state == STATE_HEADER :
                tokens = re.split(r', ', line)
                for token in tokens:
                    m = re.search(r'(.+):\s+(.+)', token)
                    if m :
                        key = m.group(1)
                        val = m.group(2)
                        config[key] = val
            elif state == STATE_RECORD :
                m = re.search(r'([\d\.]+)\s+([0-9A-Fa-f:]{17})\s+(.+?)', line)
                if m :
                    ip_addr = m.group(1)
                    mac_addr = m.group(2)
                    vendor   = m.group(3)
                    records[ip_addr] = mac_addr
                pass
            
            # post proc
            if state == STATE_INIT :
                pass
            elif state == STATE_HEADER :
                pass
            elif state == STATE_RECORD :
                pass

        fp_in.close()

    #print(config)
    #print(records)

    hostname = config['HOSTNAME']

    fp.write(
        json.dumps(
            {
                hostname : {
                    'config' : config,
                    'records': records,
                }
            },
            indent=4,
            ensure_ascii=False,
            sort_keys=True,
        )
    )

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()


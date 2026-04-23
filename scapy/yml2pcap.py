#!/usr/bin/env python3

import sys

import getopt
import json

import yaml
from scapy.all import Ether, IP, TCP, UDP, Raw, sendp, wrpcap

import random

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def merge_dict_arrays(dict1, dict2):
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        raise TypeError("Both inputs must be dictionaries.")

    merged = {}

    # Get all unique keys from both dictionaries
    all_keys = set(dict1.keys()) | set(dict2.keys())

    for key in all_keys:
        val1 = dict1.get(key, [])
        val2 = dict2.get(key, [])

        # Ensure both values are lists before merging
        if not isinstance(val1, list) or not isinstance(val2, list):
            raise ValueError(f"Values for key '{key}' must be lists.")

        merged[key] = val1 + val2  # Append arrays

    return merged

def read_yaml(filepath):
    fp = open(filepath, mode='r', encoding='utf-8')
    docs = yaml.load_all(fp, Loader=yaml.loader.SafeLoader)

    data = {}

    for doc in docs:
        data = merge_dict_arrays(data, doc)

    return data

def expand_dotted_keys(record):
    res = {}

    for key, val in record.items():
        parts = key.split(".")
        current = res
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = val
    return res

def random_mac():
    o1 = random.randint(0, 255)
    o2 = random.randint(0, 255)
    o3 = random.randint(0, 255)
    o4 = random.randint(0, 255)
    o5 = random.randint(0, 255)
    o6 = random.randint(0, 255)

    res = ''
    res += "{0:02d}".format(o1)
    res += ":{0:02d}".format(o2)
    res += ":{0:02d}".format(o3)
    res += ":{0:02d}".format(o4)
    res += ":{0:02d}".format(o5)
    res += ":{0:02d}".format(o6)
    return res

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:i:",
            [
                "help",
                "version",
                "output=",
                "iface=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
	
    output = None
    iface = None
	
    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-i", "--iface"):
            iface = a
        else:
            assert False, "unknown option"
	
    if output is None :
        print("no output option")
        ret += 1
	
    if ret != 0:
        sys.exit(1)
    
    #fp = open(output, mode='w', encoding='utf-8')
	
    packets = []

    for ymlfile in args:
        data = read_yaml(ymlfile)
        items = data['packets']
        for item in items:
            ecs = expand_dotted_keys(item)

            srcip  = ecs['source']['ip']
            sport  = ecs['source']['port']

            dstip  = ecs['destination']['ip']
            dport  = ecs['destination']['port']

            proto  = ecs['network']['transport'].lower()

            srcmac = random_mac()
            dstmac = random_mac()

            payload = b''
            if 'payload' in ecs:
                if 'text' in ecs['payload']:
                    payload = ecs['payload']['text'].encode()
                elif 'hex' in ecs['payload']:
                    payload = bytes.fromhex(ecs['payload']['hex'])
                else :
                    print('ERROR: invalid type in payload')
                    sys.exit(1)

            print('source: {0}:{1}'.format(srcip, sport))
            print('dest  : {0}:{1}'.format(dstip, dport))
            print('payload: {0}'.format(payload))
            print('')

            packet = Ether(src=srcmac, dst=dstmac) / IP(src=srcip, dst=dstip)

            if proto == 'tcp':
                packet = packet / TCP(sport=sport, dport=dport)
            elif protp == 'udp' :
                packet = packet / UDP(sport=sport, dport=dport)
            else :
                print('ERROR: invalid proto, {0}'.format(proto))
                sys.exit(1)

            packet = packet / Raw(load=payload)

            packets.append(packet)

    #print(json.dumps(data))
    wrpcap(output,packets)

    #fp.close()
	
if __name__ == "__main__":
	main()

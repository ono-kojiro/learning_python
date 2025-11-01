#!/usr/bin/env python3

import sys

import getopt
import json

import re

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
	
    if output is not None :
        fp = open(output, mode='w', encoding='utf-8')
    else :
        fp = sys.stdout
	
    if ret != 0:
        sys.exit(1)
   
    count = 0

    protocol_list = {

    }

    for filepath in args:
        if filepath != '-' :
            fp_in = open(filepath, mode='r', encoding='utf-8')
        else :
            fp_in = sys.stdin

        while 1:
            line = fp_in.readline()
            if not line:
                break
            line = re.sub(r'\r?\n?$', '', line)

            record = json.loads(line)
            

            if 'index' in record :
                continue
            
            data = {}

            layers = record['layers']
            info   = record['info']
            protocol = record['protocol']
            
            frame  = layers['frame']
            ip     = layers.get('ip', None)
            ipv6   = layers.get('ipv6', None)
            tcp    = layers.get('tcp', None)
            udp    = layers.get('udp', None)
            icmp   = layers.get('icmp', None)
            icmpv6 = layers.get('icmpv6', None)
            eth    = layers.get('eth', None)


            data['timestamp'] = frame['frame_frame_time_epoch']
            #protocols = frame['frame_frame_protocols']
            data['network.protocol'] = protocol

            if not protocol in protocol_list:
                protocol_list[protocol] = 0
            protocol_list[protocol] += 1

            data['network.info'] = info

            ip_src = None
            if tcp :
                data['source.port'] = tcp.get('tcp_tcp_srcport', None)
                data['destination.port'] = tcp.get('tcp_tcp_dstport', None)
            
            if udp :
                data['source.port'] = udp.get('udp_udp_srcport', None)
                data['source.port'] = udp.get('udp_udp_dstport', None)
            
            if icmp :
                data['icmp.type'] = icmp.get('icmp_icmp_type', None)

            if ipv6 :
                data['source.ip'] = ipv6.get('ipv6_ipv6_src', None)
                data['destination.ip'] = ipv6.get('ipv6_ipv6_dst', None)

            if icmpv6 :
                data['icmpv6.type'] = icmpv6.get('icmpv6_icmpv6_type', None)

            if eth:
                data['source.mac'] = eth.get('eth_eth_src', None)
                data['destination.mac'] = eth.get('eth_eth_dst', None)

            if ip :
                data['source.ip'] = ip.get('ip_ip_src', '')
                data['destination.ip'] = ip.get('ip_ip_dst', '')

            if not 'source.ip' in data and not 'source.mac' in data:
                print('WARN: no source.ip/source.mac in {0}'.format(protocol))

            #print('count {0}'.format(count))
            #count += 1

            fp.write(json.dumps(data, ensure_ascii=False) + '\n')

        if filepath != '-' :
            fp_in.close()
	
    if output is not None :
        fp.close()

    print(protocol_list)

	
if __name__ == "__main__":
	main()

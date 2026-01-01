#!/usr/bin/env python3

import sys

import getopt
import json

import re
import yaml

import copy

from pprint import pprint

#from Agent import Agent
from Edge import Edge
from Terminal import Terminal
from Agent import Agent

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def read_json(filepath) :
    with open(filepath, mode='r', encoding='utf-8') as fp :
        data = json.loads(fp.read())
        return data

def read_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    tmp = yaml.load(fp, Loader=yaml.loader.SafeLoader)
    data = copy.deepcopy(tmp)
    fp.close()

    return data

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
            [
                "help",
                "version",
                "output="
            ]
        )
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

    configs = read_yaml('./config.yml')

    header = '''
digraph mygraph {
    rankdir = "LR";
    ordering = out;

    //nodesep = "0.1";
    ranksep = "0.3";

    //splines = true;
    splines = curved;

    overlap = false;

    //newrank = true;

    '''

    footer = '''
}

    '''

    fp.write(header)

    data = {}
    for jsonfile in args:
        data = read_json(jsonfile)
        agents = data['agents']
        a2a = data['agent2agent']
        a2t = data['agent2terminal']

        conns = copy.deepcopy(a2a)
        conns.extend(a2t)

        # draw agents
        for agent in agents :
            agent_ip = agent['ip']
            agent_mac = agent['mac']
            a = Agent(agent_ip, agent_mac)
            a.print(fp, conns, configs)

        agent_list = {}
        for agent in agents :
            agent_list[agent['ip']] = 1
      
        fp.write('   // plot other node\n')
        mac_list = {}
        for conn in a2t:
            mac   = conn['dst_mac']
            ip    = conn['dst_ip']
            mac_list[mac] = ip

        # plot other node
        #for conn in conns :
        for mac in mac_list :
            ip = mac_list[mac]
            lines = []
            if ip :
                label = ip
                cluster = re.sub(r'\.', '_', ip)
            else :
                label = mac
                cluster = re.sub(r'\:', '_', mac)

            if label in agent_list :
                dst_port = configs['default_idx'][label]
            else :
                dst_port = "1"

            terminal = Terminal(ip, mac, dst_port)
            terminal.print(fp)

        # agents
        # draw edge
        fp.write('   // draw edge\n')
        for conn in conns :
            src_ip   = conn['src_ip']
            src_port = conn['src_port']
            mac   = conn['dst_mac']
            ip    = conn['dst_ip']
           
            default_idx = configs['default_idx'][src_ip]
            if src_port == default_idx :
                continue
            
            dst_port = "1"
            if ip in configs['default_idx']:
                dst_port = configs['default_idx'][ip]
                
            edge = Edge(src_ip, src_port, mac, ip, dst_port)
            edge.print(fp)

    fp.write(footer)

    if output is not None :
        fp.close()

if __name__ == "__main__":
    main()

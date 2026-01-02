#!/usr/bin/env python3

import sys

import getopt
import json

import re
import yaml

import copy

from pprint import pprint

from Graph import Graph

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

    graph = Graph()

    configs = read_yaml('./config.yml')

    graph.set_configs(configs)
    
    graph.print_header(fp)

    data = {}
    for jsonfile in args:
        data = read_json(jsonfile)
        agents = data['agents']
        a2a = data['agent2agent']
        a2t = data['agent2terminal']

        conns = a2a + a2t
        graph.set_connections(conns)

        # draw agents
        for agent in agents :
            agent_ip = agent['ip']
            agent_mac = agent['mac']
            a = Agent(agent_ip, agent_mac)
            graph.add_agent(a)

        graph.print_agents(fp)

        # plot other node
        for conn in a2t:
            mac = conn['dst_mac']
            ip  = conn['dst_ip']
            dst_port = "1"

            terminal = Terminal(ip, mac, dst_port)

            graph.add_terminal(terminal)

        graph.print_terminals(fp)
        #    terminal.print(fp, configs)

        # agents
        # draw edge
        for conn in conns :
            src_ip   = conn['src_ip']
            src_port = conn['src_port']
            dst_mac   = conn['dst_mac']
            dst_ip    = conn['dst_ip']
           
            if src_ip in configs['nodes'] : 
                config = configs['nodes'][src_ip]
                uplink = config.get('uplink', None)
                draw_uplink_edge = config.get('draw_uplink_edge', None)

                if src_port == uplink and draw_uplink_edge != True:
                    continue
                else :
                    is_uplink = True
            
            dst_port = "1"
            # if dst is Agent, use uplink port number
            if dst_ip in configs['nodes']:
                uplink = configs['nodes'][dst_ip]['uplink']
                dst_port = uplink
                
            edge = Edge(src_ip, src_port, dst_mac, dst_ip, dst_port)
            graph.add_edge(edge)
            #edge.print(fp)

    graph.print(fp)

    if output is not None :
        fp.close()

if __name__ == "__main__":
    main()

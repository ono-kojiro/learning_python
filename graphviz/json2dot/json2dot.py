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
from Port import Port

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
    
    data = {}

    all_ports = []

    for jsonfile in args:
        data = read_json(jsonfile)
        agents = data['agents']
        a2a = data['agent2agent']
        a2t = data['agent2terminal']

        conns = a2a + a2t

        # agents
        for agent in agents :
            agent_ip = agent['ip']
            agent_mac = agent['mac']
            uplink = configs['nodes'][agent_ip]['uplink']

            dports = []
            for conn in conns :
                if conn['src_ip'] != agent_ip :
                    continue
                port = conn['src_port']
                if port == uplink :
                    continue

                # get all pnum from dports and create list
                port_list = [ item.pnum for item in dports ]
                if not port in port_list :
                    dport = Port(None, agent_ip, port, Port.TYPE_AGENT)
                    dports.append(dport)
            
            imagepath = None
            if agent_mac in configs['images'] :
                imagepath = configs['images'][agent_mac]

            uport = Port(agent_mac, agent_ip, uplink, Port.TYPE_AGENT)

            a = Agent(uport, dports, imagepath)
            graph.add_agent(a)

            all_ports.extend([ uport ])
            all_ports.extend(dports)

        # edges
        for conn in conns :
            src_ip   = conn['src_ip']
            src_port = conn['src_port']
            dst_mac   = conn['dst_mac']
            dst_ip    = conn['dst_ip']

            dst_port = "1"

            target = None
            for port in all_ports :
                if port.ip == src_ip and port.pnum == src_port :
                    target = port
                    break

            if target is None :
                print('WARN: no port found, {0}, {1}'.format(src_ip, src_port))
                sys.exit(1)

            # add
            #sport = Port(None, src_ip, src_port)
            sport = target

            sport.set_uplink(False)
            dport = Port(dst_mac, dst_ip, dst_port)


            is_src_port_uplink = False
            is_available = True

            if src_ip in configs['nodes'] : 
                config = configs['nodes'][src_ip]
                uplink = config.get('uplink', None)

                if src_port == uplink :
                    is_src_port_uplink = True
                    # add
                    sport.set_uplink(True)

                draw_uplink_edge = config.get('draw_uplink_edge', None)
                if is_src_port_uplink and draw_uplink_edge != True:
                    is_available = False
            
            # if dst is Agent, use uplink port number
            if dst_ip in configs['nodes']:
                uplink = configs['nodes'][dst_ip]['uplink']
                dst_port = uplink

                # add
                dport.set_pnum(uplink)
                
            #edge = Edge(src_ip, src_port, dst_mac, dst_ip, dst_port, \
            #            is_src_port_uplink, is_available)
            edge = Edge(sport, dport, is_available)
            graph.add_edge(edge)
        
        # terminals
        for conn in a2t:
            mac = conn['dst_mac']
            ip  = conn['dst_ip']
            dst_port = "1"

            imagepath = None
            if mac in configs['images'] :
                imagepath = configs['images'][mac]
            
            dport = Port(mac, ip, dst_port, Port.TYPE_TERMINAL)

            edge = graph.get_edge_by_dst_mac(mac)

            terminal = Terminal(dport, imagepath, \
                    edge.sport.is_uplink)

            graph.add_terminal(terminal)

        # swap edge
        for edge in graph.edges :
            if edge.sport.is_uplink :
                tmp = edge.sport
                edge.sport = edge.dport
                edge.dport = tmp

                for terminal in graph.terminals :
                    if terminal.dport.mac == edge.sport.mac :
                        terminal.port_order = 1

    graph.print(fp)

    if output is not None :
        fp.close()

if __name__ == "__main__":
    main()

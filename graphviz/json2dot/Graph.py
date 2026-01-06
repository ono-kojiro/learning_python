import sys
import re

from Port import Port

class Graph() :
    def __init__(self) :
        self.rankdir = "LR"
        self.ordering = "out"
        self.nodesep = None
        self.ranksep = 0.3
        self.splines = False
        self.overlap = False

        self.subgraphs = []

        self.agents = []
        self.terminals = []
        self.edges = []

    def add_subgraph(self, subgraph) :
        self.subgraphs.append(subgraph)
    
    def add_agent(self, agent) :
        self.agents.append(agent)
    
    def print_agents(self, fp) :
        for agent in self.agents :
            agent.print(fp)

    def add_terminal(self, terminal) :
        self.terminals.append(terminal)

    def print_terminals(self, fp) :
        for terminal in self.terminals :
            terminal.print(fp)

    def add_edge(self, edge) :
        self.edges.append(edge)

    def print_edges(self, fp):
        for edge in self.edges :
            edge.print(fp)

    def get_edge_by_dst_mac(self, mac) :
        item = None
        for edge in self.edges :
            if edge.dport.mac == mac :
                item = edge
                break
        return item

    def print(self, fp) :
        self.print_header(fp)
        self.print_agents(fp)
        self.print_terminals(fp)
        self.print_edges(fp)
        self.print_footer(fp)
    
    def print_header(self, fp) :
        header = '''\
digraph mygraph {
    rankdir = "LR";
    ordering = out;

    //nodesep = "0.1";
    ranksep = "0.3";

    //splines = true;
    //splines = curved;
    splines = false;

    overlap = false;

    //newrank = true;

'''
        fp.write(header)
   
    def print_footer(self, fp) :
        footer = '''
}

'''
        fp.write(footer)



import sys
import re

import copy

DST_TYPE_TERMINAL = 0
DST_TYPE_AGENT = 1

class Edge() :
    def __init__(self, src_ip, src_port, dst_mac, dst_ip, dst_port,
                 is_src_port_uplink, is_available) :
        self.indent = 1
        self.minlen = 5
        self.fp = sys.stdout

        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_mac = dst_mac
        self.dst_ip = dst_ip
        self.dst_port = dst_port

        self.is_src_port_uplink = is_src_port_uplink
        self.is_available = is_available

        self.dst_type = DST_TYPE_TERMINAL

    def set_dst_type(dst_type) :
        self.dst_type = dst_type

    def print(self, fp) :
        src_cluster = re.sub(r'\.', '_', self.src_ip)
        src = "node_{0}_port{1}".format(src_cluster, self.src_port)

        if self.dst_ip :
            dst_cluster = re.sub(r'\.', '_', self.dst_ip)
        else :
            dst_cluster = re.sub(r'\:', '_', self.dst_mac)

        dst = "node_{0}_port{1}".format(dst_cluster, self.dst_port)

        portpos = 'e' # east

        line  = ' ' * self.indent * 4
        if self.dst_type == DST_TYPE_AGENT :
            tmp = src
            src = dst
            dst = tmp

        line += '"{0}":{1} -> "{2}"'.format(src, portpos, dst)
        if self.minlen :
            line += ' [minlen={0}]'.format(self.minlen)
        line += ';'

        if self.is_available :
            fp.write(line + '\n')



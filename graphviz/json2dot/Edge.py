import sys
import re

class Edge() :
    def __init__(self, src_ip, src_port, dst_mac, dst_ip, dst_port) :
        self.indent = 1
        self.minlen = 5
        self.fp = sys.stdout

        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_mac = dst_mac
        self.dst_ip = dst_ip
        self.dst_port = dst_port

    def print(self, fp) :
        src_cluster = re.sub(r'\.', '_', self.src_ip)
        src = "node_{0}_port{1}".format(src_cluster, self.src_port)

        if self.dst_ip :
            dst_cluster = re.sub(r'\.', '_', self.dst_ip)
        else :
            dst_cluster = re.sub(r'\:', '_', self.dst_mac)

        dst = "node_{0}_port{1}".format(dst_cluster, self.dst_port)

        line  = ' ' * self.indent * 4
        line += '"{0}" -> "{1}"'.format(src, dst)
        if self.minlen :
            line += ' [minlen={0}]'.format(self.minlen)
        line += ';'
        fp.write(line + '\n')


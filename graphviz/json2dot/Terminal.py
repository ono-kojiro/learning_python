import sys
import re

class Terminal() :
    def __init__(self, ip, mac, dst_port, imagepath, is_src_port_uplink) :
        self.ip  = ip
        self.mac = mac
        self.dst_port = dst_port
        self.indent = 1
        
        self.imagepath = imagepath
        self.is_src_port_uplink = is_src_port_uplink

    def print(self, fp) :
        ip = self.ip
        mac = self.mac
        dst_port = self.dst_port
        imagepath = self.imagepath

        lines = []
        if ip :
            label = ip + '\n' + mac
            cluster = re.sub(r'\.', '_', ip)
        else :
            label = mac
            cluster = re.sub(r'\:', '_', mac)

        if imagepath is None : 
            imagepath='icons/doc_jpg/pc.png'

        lines.append('subgraph cluster_{0} {{'.format(cluster))
        lines.append('    label = "{0}";'.format(label))
        lines.append('    node_{0}_image ['.format(cluster))
        lines.append('        shape=none')
        lines.append('        image="{0}"'.format(imagepath))
        lines.append('        label=""')
        lines.append('        fixedsize=true')
        lines.append('        imagescale=width')
        lines.append('    ];'.format(cluster))
        lines.append('    node_{0}_port{1} ['.format(cluster, dst_port))
        lines.append('        shape=box')
        lines.append('        label="1"')
        lines.append('        fixedsize=true')
        lines.append('        width=0.3')
        lines.append('        height=0.3')
        lines.append('    ];')

        lines.append('    node_{0}_dummy ['.format(cluster))
        lines.append('        style=invisible')
        lines.append('        shape=box')
        lines.append('        label=""')
        lines.append('        fixedsize=true')
        lines.append('        width=0.3')
        lines.append('        height=0.3')
        lines.append('    ];')
        lines.append('    node_{0}_port1 -> node_{0}_image [color=none, weight=100, len=0.3];'.format(cluster))
        lines.append('    node_{0}_image -> node_{0}_dummy [color=none ];'.format(cluster))
        lines.append('};')

        indent = ' ' * self.indent * 4
        for line in lines :
            fp.write("{0}{1}".format(indent, line))
            fp.write('\n')
        fp.write('\n')


import sys
import re

import copy

class Agent() :
    def __init__(self, ip, mac) :
        self.ip  = ip
        self.mac = mac
        self.indent = 1
        self.minlen = 4
    
    def get_downlink_ports(self, uplink, conns):
        ports = []
        for conn in conns :
            if conn['src_ip'] != self.ip :
                continue

            port = conn['src_port']
            if port == uplink :
                continue

            if not port in ports :
                ports.append(port)

        return sorted(ports)

    def print(self, fp, conns, configs) :
        indent = self.indent
        minlen = self.minlen

        agent_ip = self.ip
        agent_mac = self.mac
        
        uplink = configs['nodes'][agent_ip]['uplink']
        ports = self.get_downlink_ports(uplink, conns)

        lines = []
        cluster = re.sub(r'\.', '_', agent_ip)
        lines.append('subgraph cluster_{0} {{'.format(cluster))
        lines.append('    label = "{0}\\n{1}";'.format(agent_ip, agent_mac))
        lines.append('')
        lines.append('    node_{0}_image ['.format(cluster))
        lines.append('        shape=none')
        lines.append('        image="icons/doc_jpg/small_hub.png"')
        lines.append('        label=none')
        lines.append('    ];'.format(cluster))
            
       
        lines.append('')
        # uplink port and downlink port
        for port in [ uplink ] + ports:
            line  = '    '
            line += 'node_{0}_port{1} ['.format(cluster, port)
            line += '  shape=rectangle label="{0}"'.format(port)
            lines.append(line)
                    
            line  = '    '
            line += '  fixedsize=true'
            line += '  width=0.3 height=0.3 ];'
            lines.append(line)

        lines.append('')
        lines.append('    {')
        lines.append('        rank = same;')

        # downlink port only
        for port in ports:
             line  = '        '
             line += 'node_{0}_port{1};'.format(cluster, port)
             lines.append(line)
        
        lines.append('    }')
        lines.append('')

        line  = '    '
        line += 'node_{0}_port{1} -> node_{0}_image [color=none];'.format(cluster, uplink)
        lines.append(line)

        for port in ports:
            line  = '    '
            line += 'node_{0}_image -> node_{0}_port{1} [color=none];'.format(cluster, port)
            lines.append(line)
        
        lines.append('')
        src = None
        dst = None
        for port in ports:
            dst = port
            if src is None:
                src = dst
                continue

            line  = '    '
            line += 'node_{0}_port{1} -> node_{0}_port{2} [color=none,minlen={3}];'.format(cluster, src, dst, minlen)
            lines.append(line)
            src = dst

        lines.append('    // end of subgraph')
        # end of subgraph
        lines.append('}')

        for line in lines :
            fp.write(' ' * indent * 4)
            fp.write(line)
            fp.write('\n')
        fp.write('\n')


import sys
import re

class Agent() :
    def __init__(self, ip, mac) :
        self.ip  = ip
        self.mac = mac
        self.indent = 1
        self.minlen = 1

    def print(self, fp, conns, configs) :
        indent = self.indent
        minlen = self.minlen

        agent_ip = self.ip
        agent_mac = self.mac
        
        default_idx = configs['default_idx'][agent_ip]
        idxs = {}
        for conn in conns :
            if conn['src_ip'] == agent_ip :
                idx = conn['src_port']
                idxs[idx] = 1
        
        ports = []
        for idx in idxs:
            if default_idx != idx :
                ports.append(idx)

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
        for idx in idxs:
            line  = '    '
            line += 'node_{0}_port{1} ['.format(cluster, idx)
            line += '  shape=rectangle label="{0}"'.format(idx)
            lines.append(line)
                    
            line  = '    '
            line += '  fixedsize=true'
            line += '  width=0.3 height=0.3 ];'
            lines.append(line)

        lines.append('')
        lines.append('    {')
        lines.append('        rank = same;')

        #for idx in idxs:
        #    if default_idx != idx :
        #        line  = '        '
        #        line += 'node_{0}_port{1};'.format(cluster, idx)
        #        lines.append(line)

        for port in ports:
             line  = '        '
             line += 'node_{0}_port{1};'.format(cluster, port)
             lines.append(line)
        
        lines.append('    }')
        lines.append('')

        line  = '    '
        line += 'node_{0}_port{1} -> node_{0}_image;'.format(cluster, default_idx)
        lines.append(line)

        for idx in idxs:
            if default_idx == idx :
                continue

            line  = '    '
            line += 'node_{0}_image -> node_{0}_port{1};'.format(cluster, idx)
            lines.append(line)

        # end of subgraph
        lines.append('}')

        for line in lines :
            fp.write(' ' * indent * 4)
            fp.write(line)
            fp.write('\n')
        fp.write('\n')


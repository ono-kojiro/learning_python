import sys
import re

class Agent() :
    def __init__(self, ip, mac) :
        self.ip  = ip
        self.mac = mac
        self.indent = 1

    def print(self, fp, conns, configs) :
        agent_ip = self.ip
        agent_mac = self.mac

        lines = []
        cluster = re.sub(r'\.', '_', agent_ip)
        lines.append('    subgraph cluster_{0} {{'.format(cluster))
        lines.append('        label = "{0}\\n{1}";'.format(agent_ip, agent_mac))

        lines.append('        node_{0}_image ['.format(cluster))
        lines.append('            shape=none')
        lines.append('            image="icons/doc_jpg/small_hub.png"')
        lines.append('            label=none')
        lines.append('        ];'.format(cluster))
            
        idxs = {}
        for conn in conns :
            if conn['src_ip'] == agent_ip :
                idx = conn['src_port']
                idxs[idx] = 1
       
        for idx in idxs:
            line = '        '
            line += 'node_{0}_port{1} ['.format(cluster, idx)
            line += ' shape=rectangle label="{0}"'.format(idx)
            lines.append(line)
                    
            line = '            '
            line += 'fixedsize=true'
            line += ' width=0.3 height=0.3 ];'
            lines.append(line)

        lines.append('        {')
        lines.append('            rank = same;')

        default_idx = configs['default_idx'][agent_ip]

        for idx in idxs:
            if default_idx != idx :
                line = '            '
                line += 'node_{0}_port{1};'.format(cluster, idx)
                lines.append(line)
        lines.append('        }')
        lines.append('')

        line =  '        '
        line += 'node_{0}_port{1} -> node_{0}_image;'.format(cluster, default_idx)
        lines.append(line)

        for idx in idxs:
            if default_idx == idx :
                continue

            line  = '        '
            line += 'node_{0}_image -> node_{0}_port{1};'.format(cluster, idx)
            lines.append(line)
        lines.append('')

        # end of subgraph
        lines.append('    }')

        for line in lines :
            fp.write(line)
            fp.write('\n')
        fp.write('\n')


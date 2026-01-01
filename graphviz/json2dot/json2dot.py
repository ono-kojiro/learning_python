#!/usr/bin/env python3

import sys

import getopt
import json

import re
import yaml

import copy

from pprint import pprint

#from Agent import Agent

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
    fp.write('\n')

    data = {}
    for jsonfile in args:
        data = read_json(jsonfile)
        agents = data['agents']
        #conns = data['connections']
        a2a = data['agent2agent']
        a2t = data['agent2terminal']

        pprint(a2a)

        conns = copy.deepcopy(a2a)
        conns.extend(a2t)
        pprint(conns)

        # draw agents
        for agent in agents :
            agent_ip = agent['ip']
            agent_mac = agent['mac']

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

            #for item in items :
            #    if item['agent'] == agent :
            #        idx = item['idx']
            #        mac = item['mac']
            #        ip  = item['ip']

            # end of subgraph
            lines.append('    }')

            for line in lines :
                fp.write(line)
                fp.write('\n')
            fp.write('\n')


        agent_list = {}
        for agent in agents :
            agent_list[agent['ip']] = 1
      
        pprint(agent_list)

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

            lines.append('    subgraph cluster_{0} {{'.format(cluster))
            lines.append('        label = "{0}";'.format(label))
            lines.append('        node_{0}_image ['.format(cluster))
            lines.append('            shape=none')
            lines.append('            image="icons/doc_jpg/pc.png"')
            lines.append('            label=""')
            lines.append('            fixedsize=true')
            lines.append('            imagescale=height')
            lines.append('        ];'.format(cluster))
            lines.append('        node_{0}_port{1} ['.format(cluster, dst_port))
            lines.append('            shape=box')
            lines.append('            label="1"')
            lines.append('            fixedsize=true')
            lines.append('            width=0.3')
            lines.append('            height=0.3')
            lines.append('        ];')
            lines.append('        node_{0}_dummy ['.format(cluster))
            lines.append('            style=invisible')
            lines.append('            shape=box')
            lines.append('            label=""')
            lines.append('            fixedsize=true')
            lines.append('            width=0.3')
            lines.append('            height=0.3')
            lines.append('        ];')
            lines.append('        node_{0}_port1 -> node_{0}_image [color=none, weight=100, len=0.3];'.format(cluster))
            lines.append('        node_{0}_image -> node_{0}_dummy [color=none ];'.format(cluster))
            lines.append('     };')

            for line in lines :
                fp.write(line)
                fp.write('\n')
            fp.write('\n')


        # agents
        # draw edge
        fp.write('   // draw edge\n')
        for conn in conns :
            agent = conn['src_ip']
            idx   = conn['src_port']
            mac   = conn['dst_mac']
            ip    = conn['dst_ip']
           
            default_idx = configs['default_idx'][agent]
            if idx == default_idx :
                continue
                
            
            if ip and ip in agent_list :
                print('DEBUG: ip {0} is agent, continue'.format(ip))
                #continue
            else :
                #print('DEBUG: ip {0} is not agent'.format(ip))
                pass


            src_cluster = re.sub(r'\.', '_', agent)
            src = "node_{0}_port{1}".format(src_cluster, idx)

            if ip :
                dst_cluster = re.sub(r'\.', '_', ip)
            else :
                dst_cluster = re.sub(r'\:', '_', mac)
            
            dst_port = "1"
            if ip in configs['default_idx']:
                dst_port = configs['default_idx'][ip]

            dst = "node_{0}_port{1}".format(dst_cluster, dst_port)
            line = "    {0} -> {1} [minlen=5];".format(src, dst)
            #line = "    {0} -> {1} ;".format(src, dst)
            fp.write(line + '\n')

    fp.write(footer)
    fp.write('\n')

    if output is not None :
        fp.close()

if __name__ == "__main__":
    main()

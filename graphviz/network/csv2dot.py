#!/usr/bin/env python3
import csv
import getopt
import sys

import json

def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")

def detect_switch(records):
    switches = {}

    for name in records:
        record = records[name]
        swname = record['switch']
        ptname = record['port']
        if not swname in switches:
            switch = {
                'name' : swname,
                'port' : {}
            }
            switches[swname] = switch
        else :
            switch = switches[swname]

        if not ptname in switch['port']:
            switch['port'][ptname] = 1

    return switches

def detect_node(records, switches):
    nodes = {}

    for name in records:
        #if name in switches:
        #    continue
        
        node = records[name]
        nodes[name] = node

    return nodes

def print_node(fp, node):
    name = node['name']
    addr = node['addr']
    port = node['port']

    fp.write('  {0} '.format(name))
    fp.write('[ shape="box",\n')
    fp.write('  style="filled",\n')
    fp.write('  color="black",\n')
    fp.write('  fillcolor="lightgray",\n')
    fp.write('  label=<\n')
    fp.write('    <table border="0" cellborder="1" cellspacing="0" cellpadding="4">\n')
    fp.write('    <tr><td bgcolor="lightblue"><b>{0}</b></td></tr>\n'.format(name))
    fp.write('    <tr><td align="left">IP: {0}</td></tr>'.format(addr))
    fp.write('    <tr><td align="left">Port: {0}</td></tr>'.format(port))
    fp.write('    </table>\n')
    fp.write('  >];\n')

def print_digraph(fp, switches, nodes):
    fp.write('digraph G {\n')
    fp.write('  layout=sfdp;\n')
    fp.write('  ranksep=3;\n')
    fp.write('  ratio=auto;\n')
    fp.write('\n')
    fp.write('  node [shape=record];\n')
    #fp.write('  edge [dir=both];\n')
    fp.write('\n')

    for swname in switches:
        switch = switches[swname]
        fp.write('  {0} '.format(swname))
        fp.write('[ shape="box", style="filled", color="white" ];\n')
    fp.write('\n')

    for ndname in nodes :
        node = nodes[ndname]
        print_node(fp, node)
    fp.write('\n')

    for ndname in nodes :
        node = nodes[ndname]
        if 'switch' in node :
            swname = node['switch']
            fp.write('  {0} -> {1};\n'.format(ndname, swname))
    fp.write('\n')

        
    fp.write('}\n')
    
def dump_records(fp, records):
    fp.write(
        json.dumps(
            records,
            indent=4,
            ensure_ascii=False,
        )
    )
    fp.write('\n')

def dump_nodes(fp, nodes):
    fp.write(
        json.dumps(
            nodes,
            indent=4,
            ensure_ascii=False,
        )
    )
    fp.write('\n')

def dump_switches(fp, switches):
    fp.write(
        json.dumps(
            switches,
            indent=4,
            ensure_ascii=False,
        )
    )
    fp.write('\n')

def main():
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
            [
                "help",
                "version",
                "output=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None

    for option, optarg in options:
        if option == "-v":
            usage()
            sys.exit(1)
        elif option in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif option in ("-o", "--output"):
            output = optarg
        else:
            assert False, "unknown option"

    # if output == None :
    #   print('no output option')
    #   ret += 1

    if ret != 0:
        sys.exit(ret)

    if output == None:
        fp = sys.stdout
    else:
        fp = open(output, mode="w", encoding="utf-8")

    records = {}

    for csvfile in args:
        fp_in = open(csvfile, mode="r", newline="")
        reader = csv.reader(fp_in, delimiter=",", quotechar="|")

        columns = []
        for row in reader:
            if len(row) == 0:
                continue

            if len(columns) == 0:
                columns = row
                continue

            record = {}
            for i in range(len(columns)):
                key = columns[i]
                val = row[i]
                record[key] = val
            
            if 'name' in record:
                name = record['name']
            else :
                print('no name in record')
                sys.exit(1)

            records[name] = record

        fp_in.close()

    switches = detect_switch(records)
    nodes = detect_node(records, switches)
    print_digraph(fp, switches, nodes)

    #dump_nodes(sys.stderr, nodes)
    #dump_switches(sys.stderr, switches)
    #dump_records(sys.stderr, records)

    if output != None:
        fp.close()


if __name__ == "__main__":
    main()

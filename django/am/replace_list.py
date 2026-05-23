#!/usr/bin/env python3

import sys
import re

import getopt

STATE_INIT = 0
STATE_BLOCK = 1

def usage():
    print("Usage : {0} -o <output> <input>...".format(sys.argv[0]))

def main():
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:p:n:",
            [
                "help",
                "version",
                "output=",
                "project=",
                "name=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    project = None
    name = None

    for option, optarg in options:
        if option == "-v":
            usage()
            sys.exit(1)
        elif option in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif option in ("-o", "--output"):
            output = optarg
        elif option in ("-p", "--project"):
            project = optarg
        elif option in ("-n", "--name"):
            name = optarg
        else:
            assert False, "unknown option"

    if project is None:
        print('ERROR: no project option', file=sys.stderr)
        ret += 1

    if name is None:
        print('ERROR: no name option', file=sys.stderr)
        ret += 1

    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(ret)

    #ex. name = 'INSTALLED_APPS'
    regex_from = re.compile(r'^{0} = \[$'.format(name))
    regex_to   = re.compile(r'^\]$')

    for filepath in args:
        fp_in = open(filepath, mode="r", encoding="utf-8")
        state = STATE_INIT

        while 1 :
            line = fp_in.readline()
            if not line :
                break

            line = re.sub(r'\r?\n?$', '', line)

            # change state
            if state == STATE_INIT:
                m = re.search(regex_from, line)
                if m :
                    state = STATE_BLOCK
            elif state == STATE_BLOCK:
                pass

            # read value
            if state == STATE_INIT:
                fp.write(line + '\n')
            elif state == STATE_BLOCK:
                pass
            
            # post proc
            if state == STATE_INIT:
                pass
            elif state == STATE_BLOCK:
                if re.search(regex_to, line):
                    ymlfile = name.lower()
                    fp.write('{0} = yaml.safe_load(open("{1}/{2}.yml"))'.format(name, project, name.lower()))
                    fp.write('\n')
                    state = STATE_INIT
                pass

        fp_in.close()

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()


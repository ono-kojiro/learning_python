#!/usr/bin/env python3

import sys
import re
import pexpect

import getopt

def usage():
    print("Usage : {0} [options] host".format(sys.argv[0]))

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

    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(ret)

    #print('DEBUG', file=sys.stderr)

    for host in args:
        cmd = 'ssh -t {0}'.format(host)

        p = pexpect.spawn(cmd, encoding='utf-8', echo=False)
        p.logfile_read = fp
        p.logfile_send = None
        p.logfile = None

        # prompt
        patterns = [
            '^.+#',
            'More: <space>,  Quit: q or CTRL\\+Z, One line: <return>',
        ]

        cpl = p.compile_pattern_list(patterns)

        while 1:
            try:
                index = p.expect_list(cpl, timeout=-1)
                if index == 0:
                    line = sys.stdin.readline()
                    if not line :
                        break
                    line = re.sub(r'\r?\n?$', '', line)
                    p.sendline(line + '\n')
                elif index == 1:
                    #print('index 1', file=sys.stderr)
                    # More: <space>
                    p.sendline(' ')
                else :
                    pass
            except pexpect.EOF:
                break
            except pexpect.TIMEOUT:
                break

        p.close()

if __name__ == "__main__":
    main()


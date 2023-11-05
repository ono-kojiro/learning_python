#!/usr/bin/env python3
import csv
import getopt
import sys

import json

# https://gist.github.com/noxan/5845351
import random
import string
VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))

def generate_word(length):
    word = ""
    for i in range(length):
        if i % 2 == 0:
            word += random.choice(CONSONANTS)
        else:
            word += random.choice(VOWELS)
    return word

def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")

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


    vlans = [ 50, 60, 70 ]

    fp.write('id,name,addr,switch,port\n')
    for vlan in vlans :
        swname = "switch{0}".format(vlan)
        for i in range(10):
            name = generate_word(8)
            host_addr = random.randint(2,254)
            port_num  = random.randint(1,8)
            addr = "192.168.{0}.{1}".format(vlan, host_addr)
            port   = "port{0}".format(port_num)
            fp.write('{0},'.format(i))
            fp.write('{0},'.format(name))
            fp.write('{0},'.format(addr))
            fp.write('{0},'.format(swname))
            fp.write('{0}'.format(port))
            fp.write('\n')

    for i in range(len(vlans)):
        vlan = vlans[i]
        name = "switch{0}".format(vlan)
        addr = "192.168.{0}.1".format(vlan)
        port      = "port8"
        if i + 1 >= len(vlans) :
            next_vlan = vlans[0]
        else :
            next_vlan = vlans[i + 1]
        swname = "switch{0}".format(next_vlan)
        fp.write('{0},'.format(i))
        fp.write('{0},'.format(name))
        fp.write('{0},'.format(addr))
        fp.write('{0},'.format(swname))
        fp.write('{0}'.format(port))
        fp.write('\n')
        
    if output != None:
        fp.close()


if __name__ == "__main__":
    main()

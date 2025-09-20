#!/usr/bin/env python3

import sys
import getopt

import json
from jsonschema import validate, ValidationError

def read_json(filepath) :
    fp = open(filepath, mode='r', encoding='utf-8')
    data = json.load(fp)
    fp.close()
    return data

def main() :
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:s:",
            [
                "help",
                "version",
                "output=",
                "schema=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    schema_json = None
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
        elif o in ("-s", "--schema"):
            schema_json = a
        else:
            assert False, "unknown option"

    if schema_json is None:
        print('no schema option', file=sys.stderr)
        ret += 1

    if ret :
        sys.exit(ret)

    if output is not None:
        fp = open(output, mode='w', encoding='utf-8')
    else :
        fp = sys.stdout

    json_schema = read_json(schema_json)

    for filepath in args:
        print('INFO: {0}'.format(filepath), file=sys.stderr)
        fp_in = open(filepath, mode='r', encoding='utf-8')
        while 1:
            line = fp_in.readline()
            if not line:
                break
            data = json.loads(line)
            try :
                validate(data, json_schema)
            except ValidationError as e:
                print(e.message, file=sys.stderr)
        fp_in.close()
    
    if output is not None:
        fp.close()

if __name__ == '__main__' :
    main()



#!/usr/bin/env python3

import sys
import getopt

import json
from jsonschema import validate, ValidationError

def usage():
    print("Usage : {0} <OPTIONS> input.json".format(sys.argv[0]))

def read_json(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    data = json.load(fp)
    fp.close()
    return data

def main():
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

    output = None
    schema_json = None

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

    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(1)

    nerror = 0

    if schema_json is None :
        schema = read_json('schema.json')
    else :
        schema = read_json(schema_json)

    for filepath in args:
        data = read_json(filepath)
        try :
            validate(data, schema)
        except ValidationError as e:
            fp.write(e.message + "\n")
            nerror += 1

    fp.write("{0} error(s) found\n".format(nerror))
    
    if output is not None :
        fp.close()


if __name__ == "__main__" :
    main()


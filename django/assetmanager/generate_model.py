#!/usr/bin/env python3

import sys
import re

import getopt

import yaml

from pprint import pprint

def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")

def read_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    data = yaml.safe_load(fp)
    fp.close()
    return data

def render_default(k, v):
    if k == "default" and (v in [ "list", "dict" ]):
        ret = 'default={0}'.format(v)
    elif k == "on_delete":
        ret = '{0}=models.{1}'.format(k, v)
    else :
        ret = '{0}={1}'.format(k, repr(v))
    return ret

def render_simple_field(field_def):
    args = []

    for k, v in field_def.items():
        if k == "type":
            continue
        if k is None:
            k = 'null'
             
        args.append(render_default(k, v))

    return args

def render_relation_field(field_def, ftype):
    args = []

    args.append('to={0}'.format(repr(field_def['to'])))

    val = field_def.get('on_delete', 'CASCADE')
    if val.startswith("models."):
        args.append('on_delete={0}'.format(val))
    else :
        args.append('on_delete=models.{0}'.format(val))
            
    for k, v in field_def.items():
        if k in [ "type", "to", "on_delete" ]:
            continue

        if k is None:
            k = 'null'
             
        args.append(render_default(k, v))

    return args
        
def generate_related_models(fp, data):
    related = []
    for fname, field_def in data["fields"].items():
        ftype = field_def["type"]
        if ftype in [ "ForeignKey", "OneToOneField" ]:
            val = field_def["to"]
            related.append(val)
    return related

def generate_model(fp, data):
    name = data['name']

    fp.write("class {0}(models.Model):\n".format(name))
    
    for fname, field_def in data["fields"].items():
        ftype = field_def["type"]

        if ftype in [ "ForeignKey", "OneToOneField" ]:
            args = render_relation_field(field_def, ftype)
        else :
            args = render_simple_field(field_def)

        arg_str = ", ".join(args)
        fp.write('    {0} = models.{1}({2})\n'.format(fname, ftype, arg_str))

    # __str__ の自動生成
    fp.write("\n")
    fp.write("    def __str__(self):\n")

    id_field = None
    name_field = None
    address_field = None
    first_field = None

    for fname in data["fields"].keys():
        if first_field is None:
            first_field = fname
        if fname.endswith("_id"):
            id_field = fname
        if fname == "name":
            name_field = fname
        if fname == "address":
            address_field = fname

    # 優先順位: id + (name or address) → name → address → first_field
    if id_field:
        if name_field:
            fp.write(f'        return f"{{self.{id_field}}}: {{self.{name_field}}}"\n')
        elif address_field:
            fp.write(f'        return f"{{self.{id_field}}}: {{self.{address_field}}}"\n')
        else:
            fp.write(f'        return f"{{self.{id_field}}} (no IP address)"\n')
    elif name_field:
        fp.write(f'        return f"{{self.{name_field}}}"\n')
    elif address_field:
        fp.write(f'        return f"{{self.{address_field}}}"\n')
    else:
        fp.write(f'        return f"{{self.{first_field}}}"\n')


    if "meta" in data:
        fp.write("\n");
        fp.write("    class Meta:\n")
        for k, v in data["meta"].items():
            fp.write("        {0} = {1}\n".format(k, repr(v)))

def main():
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:d:",
            [
                "help",
                "version",
                "output=",
                "depend=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    depend_yaml = None

    for option, optarg in options:
        if option == "-v":
            usage()
            sys.exit(1)
        elif option in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif option in ("-o", "--output"):
            output = optarg
        elif option in ("-d", "--depend"):
            depend_yaml = optarg
        else:
            assert False, "unknown option"

    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if depend_yaml is None:
        print('ERROR: no depend option', file=sys.stderr)
        sys.exit(1)

    if ret != 0:
        sys.exit(ret)

    depend_map = read_yaml(depend_yaml)['dependencies']

    fp.write('from django.db import models\n\n')

    for filepath in args:
        fp_in = open(filepath, mode="r", encoding="utf-8")
        data = yaml.safe_load(fp_in)

        print(data, file=sys.stderr)

        name = data['name']
        deps = depend_map[name]

        #related_models = generate_related_models(fp, data)
        #for related_model in related_models:
        #    fp.write('from myapp.models import {0}\n'.format(related_model))

        for dep in deps:
            fp.write('from myapp.models import {0}\n'.format(dep))

        generate_model(fp, data)
        fp_in.close()

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()


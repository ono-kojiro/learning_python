#!/usr/bin/env python3

import os
import sys

import getopt
import json

import re
import glob

import shlex
import subprocess

from datetime import datetime, timezone, timedelta

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def get_command_result(cmd):
    args = shlex.split(cmd)
    proc = subprocess.Popen(
             args,
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE,
             text=True,
             bufsize=1,
           )

    while True:
        line = proc.stdout.readline()
        if line:
            yield line
        if not line and proc.poll() is not None:
            break

def convert_keys(obj):
    """辞書のキーを再帰的にアンダースコア→ドットに変換"""
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            # index 行は削除
            if k == "index":
                continue

            # アンダースコアをドットに変換
            new_key = k.replace("_", ".")

            new_obj[new_key] = convert_keys(v)
        return new_obj

    elif isinstance(obj, list):
        return [convert_keys(x) for x in obj]

    else:
        return obj

def nest_key_path(d, key_path, value):
    """key_path = ["tcp","tcp","options","timestamp","tsecr"] を辞書に挿入"""
    current = d
    for k in key_path[:-1]:
        if k not in current or not isinstance(current[k], dict):
            current[k] = {}
        current = current[k]
    current[key_path[-1]] = value


def convert_ek_recursive(obj):
    """辞書全体を再帰的に走査し、ドット区切りキーを階層化する"""
    if isinstance(obj, dict):
        new_obj = {}

        for key, value in obj.items():
            # index 行は削除
            if key == "index":
                continue

            # 再帰的に値を変換
            value = convert_ek_recursive(value)

            # アンダースコアをドットに変換
            key = key.replace("_", ".")

            # ドット区切りキーを階層化
            if "." in key:
                parts = key.split(".")
                nest_key_path(new_obj, parts, value)
            else:
                # 通常のキー
                new_obj[key] = value

        return new_obj

    elif isinstance(obj, list):
        return [convert_ek_recursive(x) for x in obj]

    else:
        return obj

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hvo:", ["help", "version", "output="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
	
    outroot = None

    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--outroot"):
            outroot = a
        else:
            assert False, "unknown option"
	
    if outroot is  None :
        print("no outroot option")
        ret += 1
	
    if ret != 0:
        sys.exit(1)

    jst = timezone(timedelta(hours=9))
            
    c2  = 'tshark -T fields -e frame.time_epoch -e frame.protocols'
    c2 += ' -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport'
    c2 += ' -e udp.srcport -e udp.dstport -e tcp.flags'
    c2 += ' -E header=y -E separator=, -E quote=n -E occurrence=f'
    c2 += ' -r -'

    for indir in args:
        indir = re.sub(r'/$', '', indir)

        pattern = '{0}/**/*.pcap.xz'.format(indir)
        files = sorted(glob.glob(pattern, recursive=True))
        outroot = re.sub(r'/$', '', outroot)

        for filepath in files :
            filename = os.path.basename(filepath)

            m = re.search(r'^(\d{4})(\d{2})(\d{2})-(\d{2})(\d{4})-', filename)
            if m :
                year  = m.group(1)
                month = m.group(2)
                day   = m.group(3)
                hour  = m.group(4)
            else :
                print('ERROR: invalid filename, {0}'.format(filename), file=sys.stderr)
                sys.exit(1)
            
            basename = re.sub(r'.pcap.xz$', '', filename)

            outdir = '{0}/{1}{2}/{1}{2}{3}/{1}{2}{3}-{4}'.format(
                outroot, year, month, day, hour)

            os.makedirs(outdir, exist_ok=True)

            output = '{0}/{1}.ndjson'.format(outdir, basename)
                
            print('DEBUG: input is {0}'.format(filepath), file=sys.stderr)
            
            if os.path.exists(output) :
                print('DEBUG: skip {0}'.format(output), file=sys.stderr)
                continue
            else:
                print('DEBUG: output is {0}'.format(output), file=sys.stderr)

            fp = open(output, mode='w', encoding='utf-8')

            c1 = 'xz -k -c -d {0}'.format(filepath)

            p1 = subprocess.Popen(shlex.split(c1), stdout=subprocess.PIPE)
            p2 = subprocess.Popen(shlex.split(c2), stdin=p1.stdout,
                                     stdout=subprocess.PIPE, text=True)
    
            is_first = 1

            fields = None

            for line in p2.stdout:
                line = re.sub(r'\r?\n?$', '', line)
                tokens = line.split(",")

                if is_first :
                    fields = tokens
                    is_first = 0
                    continue

                data = {}

                for i in range(len(fields)):
                    field = fields[i]
                    value = tokens[i]
                    data[field] = value

                data_str = json.dumps(data, ensure_ascii=False)

                fp.write('{0}\n'.format(data_str))

            p1.wait()
            p2.wait()

            fp.close()

if __name__ == "__main__":
	main()

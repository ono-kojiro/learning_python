#!/usr/bin/env python3

import os
import sys
import re

import getopt

import json

from sentence_transformers import SentenceTransformer
import torch

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

    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(ret)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    #device = "cpu"
    print("Using device:", device)

    model_dir = 'local-model'
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'

    if os.path.exists(model_dir):
        print('INFO: read model from {0}'.format(model_dir))
        model = SentenceTransformer(model_dir, device=device)
    else :
        # モデル読み込み
        print('INFO: download model from internet and save to {0}'.format(model_dir))
        model = SentenceTransformer(model_name, device=device)
        model.save(model_dir)

    is_start = 0
    
    for filepath in args:
        segment = ""

        fp_in = open(filepath, mode="r", encoding="utf-8")
        while 1 :
            line = fp_in.readline()
            if not line :
                break

            line = re.sub(r'\r?\n?$', '', line)

            m = re.search(r'^\*{3,}\s*(.+)\s*\*{3,}$', line)
            if m :
                line = m.group(1)
                is_start = 1
            m = re.search(r'^={40,}$', line)
            if m :
                is_start = 0

            if is_start :
                segment += line
                if len(segment) > 500:
                    vector = model.encode(segment).tolist()
                    #fp.write(segment + '\n')
                    data = json.dumps(
                        {
                            "text": segment,
                            "vector": vector,
                        },
                        ensure_ascii=False,
                    )
                    fp.write(data)
                    fp.write('\n')

                    segment = ''
                else :
                    pass

        if len(segment) > 0:
            #fp.write(segment + '\n')
            vector = model.encode(segment).tolist()
            data = json.dumps(
                {
                    "text": segment,
                    "vector": vector,
                },
                ensure_ascii=False,
            )
            fp.write(data)
            fp.write('\n')

            segment = ''

        fp_in.close()
    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()


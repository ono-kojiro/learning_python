#!/usr/bin/env python3

import sys
import os

import getopt
import json

from sentence_transformers import SentenceTransformer
import torch

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def read_json(filepath):
    fp = open(filepath, mode='r', encoding='utf-8')
    data = json.load(fp)
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
        fp = open(output, mode="a", encoding='utf-8')
    else :
        fp = sys.stdout
	
    if ret != 0:
        sys.exit(1)

    # GPU が使えるか確認
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

    for jsonfile in args:
        data = read_json(jsonfile)

        title  = data['title']
        author = data['author']
        chunks = data['chunks']

        for chunk in chunks:
            text = chunk['text']

            print("TEXT: {0}".format(text), file=sys.stderr)
            # ベクトル化
            vector = model.encode(text).tolist()
            record = {
                'text': text,
                'vector': vector,
                'title': title,
                'author': author,
                'type': chunk['type'],
            }

            fp.write(json.dumps(record, ensure_ascii=False))
            fp.write('\n')

    if output is not None :
        fp.close()
	
if __name__ == "__main__":
	main()

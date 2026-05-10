#!/usr/bin/env python3

import sys

import getopt
import yaml

import re

import json

from bs4 import BeautifulSoup

from pprint import pprint

def read_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    docs = yaml.load_all(fp, Loader=yaml.loader.SafeLoader)

    #pprint(docs)

    data = []
    for items in docs:
        for item in items:
            #pprint(item)
            data.append(item)

    fp.close()
    return data

def main() :
    ret = 0

    try:
        options, args = getopt.getopt(
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

    for option, arg in options:
        if option in ("-v", "-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = arg
        else:
            assert False, "unknown option"

    if output is not None:
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(1)

    data = {}

    for filepath in args :
        fp_in = open(filepath, mode='r', encoding='sjis')
        soup = BeautifulSoup(fp_in, "html.parser")

        for ruby in soup.find_all("ruby"):
            rb = ruby.find("rb").get_text()
            rt = ruby.find("rt").get_text()
            ruby.replace_with(f"{rb}（{rt}）")

        for h4 in soup.find_all("h4", class_="naka-midashi"):
            h4.decompose()

        title = soup.title.string.strip()
        title = soup.find("h1").get_text(strip=True)
        author = soup.find("h2").get_text(strip=True)

        main = soup.find("div", class_="main_text")
        text = main.get_text("\n")
        text = re.sub(r'[ ]+', ' ', text)
        text = re.sub(r'\n+', '\n', text)

        paragraphs = []
        for p in re.split(r'\n　', text):
            p = p.strip()
            p = re.sub(r'\s+', ' ', p).strip()
            if p :
                paragraphs.append(p)

        data['title'] = title
        data['author'] = author
        #data['text'] = text
        data['paragraphs'] = paragraphs

        fp_in.close()

    #fp.write('---\n')
    #yaml.dump(data, fp, allow_unicode=True, default_flow_style=False)
    fp.write(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False,
        )
    )

    if output is not None:
        fp.close()
        
    #for line in text.splitlines()[:10]:
    #    print(repr(line))


if __name__ == "__main__":
    main()

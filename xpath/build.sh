#!/bin/sh

find ./ -name "*.xml" -print -exec python3 read_xml.py {} \;


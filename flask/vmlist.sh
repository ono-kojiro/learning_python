#!/bin/sh

sudo vm list | python3 vmlist.py - > vmlist.json


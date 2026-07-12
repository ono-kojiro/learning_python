import os

DEBUG = os.environ.get("VERBOSE", "0") != "0"

def debug(msg):
        print(msg)


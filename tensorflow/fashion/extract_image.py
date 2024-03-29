#!/usr/bin/env python3
import getopt
import gzip
import sys

import numpy as np
from PIL import Image



def usage():
    print(f"usage : {sys.argv[0]} [options] images")
    msg = """
  options:
    -n, --number     id of target image
    -o, --output     output filepath
"""
    print(msg)


def export_image(output, filepath, number):
    # filepath = 'fashion-mnist/data/fashion/train-images-idx3-ubyte'

    count = 28 * 28
    offset = 16 + 28 * 28 * number

    fp = gzip.open(filepath, "rb")
    image = np.frombuffer(fp.read(), dtype=np.uint8, count=count, offset=offset)
    image = image.reshape((28, 28))
    fp.close()

    Image.fromarray(image).save(output)

    print(f"saved {output}")


def main():
    ret = 0
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:n:",
            [
                "help",
                "version",
                "output=",
                "number=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    number = None

    for opt, arg in opts:
        if opt == "-v":
            usage()
            sys.exit(1)
        elif opt in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-n", "--number"):
            number = int(arg)

    if output is None:
        print("no output option")
        ret += 1

    if number is None:
        print("no number option")
        ret += 1

    if ret != 0:
        sys.exit(1)

    for filepath in args:
        export_image(output, filepath, number)


if __name__ == "__main__":
    main()

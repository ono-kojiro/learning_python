#!/usr/bin/env python3

import sys
import os
import re

import getopt

import numpy as np
import matplotlib.pyplot as plt

import gzip
from PIL import Image

from pprint import pprint

def usage() :
  print('usage : {0} [options] images'.format(sys.argv[0]))
  msg = '''
  options:
    -n, --number     id of target image
    -o, --output     output filepath
'''
  print(msg)
  
def export_image(output, filepath, number) :
  #filepath = 'fashion-mnist/data/fashion/train-images-idx3-ubyte'

  count = 28 * 28
  offset = 16 + 28 * 28 * number

  if re.search(r'\.gz', filepath) :
    fp = gzip.open(filepath, 'rb')
  else :
    fp = open(filepath, 'rb')
  
  image = np.frombuffer(fp.read(), dtype=np.uint8, count=count, offset=offset)
  image = image.reshape((28, 28))

  #pprint(image)
  fp.close()

  if False :
    plt.figure()
    plt.imshow(image)
    plt.colorbar()
    plt.grid(False)
    plt.savefig(output)
  else :
    Image.fromarray(image).save(output)

  print('saved {0}'.format(output))

def main() :
  ret = 0
  try :
    opts, args = getopt.getopt(
      sys.argv[1:],
      'hvo:n:',
      [
        'help',
        'version',
        'output=',
        'number=',
      ]
    )
  except getopt.GetoptError as err:
    print(str(err))
    sys.exit(1)

  output = None
  number = None

  for opt, arg in opts :
    if opt == '-v' :
      usage()
      sys.exit(1)
    elif opt in ('-h', '--help') :
      usage()
      sys.exit(1)
    elif opt in ('-o', '--output') :
      output = arg
    elif opt in ('-n', '--number') :
      number = int(arg)

  if output is None :
    print('no output option')
    ret += 1
  
  if number is None :
    print('no number option')
    ret += 1

  if ret != 0 :  
    sys.exit(1)

  for filepath in args :
    export_image(output, filepath, number)

if __name__ == '__main__' :
  main()



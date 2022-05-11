#!/usr/bin/env python3

import sys
import getopt

from PIL import Image

import pyocr
import pyocr.builders

def usage() :
  print('usage : {0} [<options>] input.img'.format(sys.argv[0]))

def main() :
  ret = 0
  try :
    opts, args = getopt.getopt(
      sys.argv[1:],
      'hvo:',
      [
        'help',
        'version',
        'output=',
      ]
    )
  except getopt.GetoptError as err:
    print(str(err))
    sys.exit(1)

  output = None

  for opt, arg in opts:
    if opt in ('-v', '--version') :
      usage()
      sys.exit(1)
    elif opt in ('-h', '--help') :
      usage()
      sys.exit(1)
    elif opt in ('-o', '--output') :
      output = arg

  if len(args) == 0 :
    print('ERROR : no input images')
    sys.exit(1)

  if output is not None :
    fp = open(output, mode='w')
  else :
    fp = sys.stdout

  tools = pyocr.get_available_tools()
  if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

  tool = tools[0]
  print("Will use tool '%s'" % (tool.get_name()))

  for filepath in args :
    txt = tool.image_to_string(
      Image.open(filepath),
      lang="jpn",
      builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    fp.write(txt)
  
  if output is not None :
    fp.close

if __name__ == '__main__' :
  main()


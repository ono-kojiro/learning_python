#!/usr/bin/env python3
import sys
import os

import getopt

# https://www.tensorflow.org/tutorials/keras/classification?hl=ja

import tensorflow as tf
from tensorflow import keras

import numpy as np

from pprint import pprint

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
  
  fashion_mnist = tf.keras.datasets.fashion_mnist
  (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
  train_images, test_images = train_images / 255.0, test_images / 255.0

  model = tf.keras.models.load_model('models/my_model')

  test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
  print('test loss    : {0}'.format(test_loss))
  print('test accurary: {0}'.format(test_acc))

if __name__ == '__main__' :
  main()


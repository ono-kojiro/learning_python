#!/bin/sh

cat - << 'EOS' | ./run.py -
{
  echo Hello World
}
EOS


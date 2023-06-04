#!/bin/sh

mac="123456778ABC"

# https://perldoc.jp/docs/perl/5.36.0/perlretut.pod#Looking32ahead32and32looking32behind

echo $mac | perl -p -e 's/(..)(?!$)/$1:/g'


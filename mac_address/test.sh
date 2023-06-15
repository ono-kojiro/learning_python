#!/bin/sh

mac="123456789ABC"

# https://perldoc.jp/docs/perl/5.36.0/perlretut.pod#Looking32ahead32and32looking32behind

echo Perl
echo $mac | perl -p -e 's/(..)(?!$)/$1:/g'

echo Python
#python3 test.py $mac
echo 123456789ABC | python -c 'import re,sys; str=re.sub(r"(..)(?!$)","\\1:",sys.stdin.readline()); print(str)'


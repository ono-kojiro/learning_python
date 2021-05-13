#!/bin/sh

echo This is stderr data. 1>&2

echo 1..5
echo ok 1 - first test

echo This is stdout data.

echo ok 2 - second test

echo skipping test. 1>&2
echo ok 3 - third test # skip : skip third test

echo todo test. 1>&2
echo ok 4 - fourth test. # todo : this test

echo ok 5 - fifth test


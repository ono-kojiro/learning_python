#!/usr/bin/env sh

echo "1..1"

python3 build/lib/example.py \
  spdx-examples/example1/spdx/example1.spdx

if [ $? -eq 0 ]; then
  echo "ok"
else
  echo "not ok"
fi



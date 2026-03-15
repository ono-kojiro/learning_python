#!/usr/bin/env python3

import shlex
import subprocess

cmd="df -h"
args = shlex.split(cmd)

proc = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
       )

for line in proc.stdout:
    print("LINE: {0}".format(line.strip()))

proc.wait()


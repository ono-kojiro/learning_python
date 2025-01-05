#!/usr/bin/env python3

import sys
import re
import pexpect

p = pexpect.spawn('ssh -t cisco', encoding='utf-8', echo=False)
p.logfile_read = sys.stdout
p.logfile_send = None
p.logfile = None

# prompt
pattern = '^.+#'
    
cpl = p.compile_pattern_list([pattern])

while 1:
    try:
        index = p.expect_list(cpl, timeout=-1)
        if index == 0:
            line = sys.stdin.readline()
            if not line :
                break
            line = re.sub(r'\r?\n?$', '', line)
            p.sendline(line + '\n')
        else :
            pass
    except pexpect.EOF:
        break
    except pexpect.TIMEOUT:
        break

p.close()


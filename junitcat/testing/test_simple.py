import os
import junitcat

import tempfile

import pytest

from pprint import pprint

def test_simple():
    lines = '''<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" errors="0" failures="0" skipped="0" tests="1">
    <testcase name="simple" />
  </testsuite>
</testsuites>
'''

    fd, filepath = tempfile.mkstemp(suffix=".xml")
    os.write(fd,lines.encode())
    os.close(fd)
    ret = junitcat.validate_junit_xml("junit-10.xsd", filepath)
    assert ret == 0

    os.remove(filepath)



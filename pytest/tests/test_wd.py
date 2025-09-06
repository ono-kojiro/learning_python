import pytest

def test_output():
    fp = open('test_output.txt', mode='w', encoding='utf-8')
    fp.write('Hello World\n')
    fp.close()


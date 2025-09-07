import pytest
import sys
import json

from pprint import pprint

from vega import Autosize1, Autosize
from vega import Data
from vega import Signal, Signal1, Signal2, Signal3
from vega import Padding, Padding1, Padding2
from vega import Mark
from vega import Scale
from vega import Scope
from vega import VegaVisualizationSpecificationLanguage
from vega import Encode
from vega import EncodeEntry

def read_json(filepath):
    fp = open(filepath, mode='r', encoding='utf-8')
    data = json.load(fp)
    fp.close()
    return data

def write_json(filepath, json_str):
    fp = open(filepath, mode='w', encoding='utf-8')
    fp.write(json_str)
    fp.write('\n')
    fp.close()

data = read_json('Spec.json')

def test_marks() :
    marks = data['marks']
    for item in marks :
        mark = Mark.model_validate(item)
        #write_json('scope.json', scope.model_dump_json(indent=2))
        print('name: {0}'.format(mark.name))
        if mark.encode is not None :
            print('encode')
            print(mark)
            encode = EncodeEntry.model_validate(item['encode'])
    pass


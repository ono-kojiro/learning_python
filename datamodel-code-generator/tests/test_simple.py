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

def read_json(filepath):
    fp = open(filepath, mode='r', encoding='utf-8')
    data = json.load(fp)
    fp.close()
    return data

data = read_json('Spec.json')

def test_autosize() :
    autosize = Autosize(data['autosize']) 
    pprint(autosize)

def test_signal() :
    for item in data['signals']:
        signal = Signal.model_validate(item)
        print(signal)

def test_padding() :
    #padding = Padding(data['padding'])
    padding = Padding.model_validate(data['padding'])

def test_mark() :
    for item in data['marks']:
        mark = Mark(type=item['type'], input_value=item)
        pprint(mark)

def test_scale() :
    for item in data['scales']:
        scale = Scale.model_validate(item)

def test_scope() :
    scope = Scope.model_validate(data)
    
def test_spec() :
    spec = VegaVisualizationSpecificationLanguage()


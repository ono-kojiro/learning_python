#!/usr/bin/env python3

import sys
import os

import re
import json

import tomllib
from ollama import chat
from ollama import ChatResponse

from pprint import pprint

def run_basic(model, query):
    messages = [
        {
            'role': 'user',
            'content': query,
        },
    ]
    res: ChatResponse = chat(model=model, messages=messages)
    print(res.message.content)
    print('')

def run_stream(model, query):
    messages = [
        {
            'role': 'user',
            'content': query,
        },
    ]
    stream = chat(model,
        messages=messages,
        stream=True)
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
    print('')

def main():
    model = 'hf.co/alfredplpl/gemma-2-baku-2b-it-gguf:latest'
    query = '空はなぜ青いのですか?'
    
    run_stream(model, query)
    return

if __name__ == "__main__" :
    main()


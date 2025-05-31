#!/usr/bin/env python3

import sys
import os

import getopt

import re
import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import tomllib
import hashlib

from pprint import pprint

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

__all__ = [
  "Client",
]

class Client():
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'Authorization': 'Bearer {0}'.format(api_key),
        }

    def set_base_url(self, base_url):
        self.base_url = base_url

    def set_api_key(self, api_key):
        self.api_key = api_key

    def get_knowledge_id(self, name):
        url = self.base_url + '/api/v1/knowledge/list'
        res = requests.get(
            url,
            headers=self.headers,
            verify=False,
        )
        items = json.loads(res.text)

        id = None
        for item in items:
            if item['name'] == name:
                id = item['id']
                break
        return id

    def get_file_hash(self, filepath):
        algorithm = 'sha256'
        h = hashlib.new(algorithm)
        l = h.block_size * 0x800
        with open(filepath, 'rb') as f:
            data = f.read(l)
            while data :
                h.update(data)
                data = f.read(l)
        return h.hexdigest()

    def get_file_id(self, filepath):
        url = self.base_url + '/api/v1/files/'
        res = requests.get(
            url,
            headers=self.headers,
            verify=False,
        )
        items = json.loads(res.text)

        digest = self.get_file_hash(filepath)
        print("DEBUG: digest is {0}".format(digest))
        id = None
        for item in items:
            pprint(item)
            if item['hash'] == digest :
                id = item['id']
                break
        return id
    
    def add_file_to_knowledge(self, name, filename):
        k_id = self.get_knowledge_id(name)
        f_id = self.get_file_id(filename)
        print('DEBUG: knowledge ID is {0}'.format(k_id))
        print('DEBUG: filename is {0}'.format(filename))
        print('DEBUG: file ID is {0}'.format(f_id))
        url = self.base_url + '/api/v1/knowledge/{0}/file/add'.format(k_id)
        payload = {
            'file_id': f_id,
        }

        res = requests.post(
            url,
            headers=self.headers,
            json=payload,
            verify=False,
        )
        text = json.loads(res.text)
        pprint(text)

        
    def add_file(self, filepath):
        url = self.base_url + '/api/v1/files/'
        files = { 'file' : open(filepath, mode='rb') }
        res = requests.post(
            url,
            headers=self.headers,
            files=files,
            verify=False,
        )
        text = json.loads(res.text)
        pprint(text)
        
    def show_models(self):
        url = self.base_url + '/api/models'
        res = requests.get(
            url,
            headers=self.headers,
            verify=False,
        )
        obj = json.loads(res.text)
        print('INFO: Models')
        for item in obj['data']:
            print('  {0}'.format(item['name']))
   
    def create_knowledge(self, name):
        ret = 1

        items = self.get_knowledges()
        for item in items:
            if item['name'] == name :
                print('ERROR: knowledge {0} is already existing'.format(name))
                return ret

        url = self.base_url + '/api/v1/knowledge/create'
        payload = {
            'name': name,
            'description': name,
        }
        res = requests.post(
            url,
            headers=self.headers,
            json=payload,
            verify=False,
        )
        if res.status_code == 200:
            ret = 0
        return ret
    
    def get_knowledges(self):
        url = self.base_url + '/api/v1/knowledge/'
        res = requests.get(
            url,
            headers=self.headers,
            verify=False,
        )
        #return json.loads(res.text)
        return res.json()

    def delete_knowledge(self, knowledge_id):
        ret = 1

        url = self.base_url + '/api/v1/knowledge/{0}/delete'.format(knowledge_id)
        headers = {
            'Authorization': 'Bearer {0}'.format(self.api_key),
        }

        res = requests.delete(
            url,
            headers=headers,
            verify=False,
            )
        
        if res.status_code == 200:
            ret = 0
        return ret

    def delete_knowledges(self):
        items = self.get_knowledges()
        for item in items:
            pprint(item)
            print('DEBUG: delete {0}'.format(item['name']))
            self.delete_knowledge(item['id'])
        
    def show_knowledges(self):
        url = self.base_url + '/api/v1/knowledge/'
        res = requests.get(
            url,
            headers=self.headers,
            verify=False,
        )
        obj = json.loads(res.text)
        print('INFO: Knowledges')
        for item in obj:
            print('  {0}'.format(item['name']))

    def show_files(self):
        url = self.base_url + '/api/v1/files/'
        res = requests.get(
            url,
            headers=self.headers,
            verify=False,
        )
        obj = json.loads(res.text)
        print('INFO: Files')
        for item in obj:
            filename = item['filename']
            id = item['id']
            print('  {0} : {1}'.format(filename, id))
            #pprint(item)
    
    def get_files(self):
        url = self.base_url + '/api/v1/files/'
        res = requests.get(
            url,
            headers=self.headers,
            verify=False,
        )
        return res.json()

    def delete_file(self, file_id):
        ret = 1

        url = self.base_url + '/api/v1/files/{0}'.format(file_id)
        headers = {
            'Authorization': 'Bearer {0}'.format(self.api_key),
        }

        res = requests.delete(
            url,
            headers=headers,
            verify=False,
            )
        
        if res.status_code == 200:
            ret = 0
        return ret
        
    def delete_files(self):
        items = self.get_files()
        for item in items:
            self.delete_file(item['id'])

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
            [
                "help",
                "version",
                "output="
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None

    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unknown option"

    if output is not None :
        fp = open(output, mode="w", encoding='utf-8')
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(ret)

    params = {}
    configfiles = [ './api_key.shrc', './config.shrc' ]
    for filepath in configfiles:
        with open(filepath, mode='rb') as f:
            params = params | tomllib.load(f)

    base_url = params['base_url']
    api_key  = params['api_key']

    client = Client(base_url, api_key)
    client.show_models()
    client.show_knowledges()
    client.show_files()
    
    if output is not None :
        fp.close()

if __name__ == "__main__" :
    main()


#!/usr/bin/env python3

import sys

import getopt

import requests
from getpass import getpass
from bs4 import BeautifulSoup

from pprint import pprint

def main() :
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:u:p:d:",
            [
              "help",
              "version",
              "output=",
              "username=",
              "password=",
              "debug=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    username = None
    password = None
    output = None

    debug = 0

    for option, arg in options:
        if option in ("-v", "-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = arg
        elif option in ("-u", "--username"):
            username = arg
        elif option in ("-p", "--password"):
            password = arg
        elif option in ("-d", "--debug"):
            debug = arg
        else:
            assert False, "unknown option"

    #if username is None :
    #    print('no username option')
    #    ret += 1

    if output is not None:
        fp = open(output, mode="wb")
    else :
        fp = sys.stdout
    
    if ret != 0:
        sys.exit(1)

    for url in args :
        session = requests.session()
        res = session.get(url)
        if debug :
            pprint(res)

        res.raise_for_status()

        soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")
        
        token = ''
        utf8 = ''
        back_url = ''

        if debug :
            print('res.encoding: {0}'.format(res.encoding))

        if res.encoding is not None :
            tag = soup.find(attrs={'name':'authenticity_token'})
            if tag :
                token = tag.get('value')

            tag = soup.find(attrs={'name':'utf8'})
            if tag :
                utf8 = tag.get('value')

            tag = soup.find(attrs={'name':'back_url'})
            if tag :
                back_url = tag.get('value')

        if back_url != '' :
            if username is None:
                username = input('Username: ')
            if password is None:
                password = getpass(prompt='Password: ')

            data = {
                "username": username,
                "authenticity_token": token,
                "utf8" : utf8,
                "back_url" : back_url,
            }

            data['password'] = password
            res = session.post(res.url, data=data, allow_redirects=True)
            res.raise_for_status()
        
        fp.write(res.content)
        session.cookies.clear()
        session.close()


if __name__ == "__main__":
    main()

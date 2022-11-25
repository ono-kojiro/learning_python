#!/usr/bin/env python3

import sys
import os
import re
import shutil
import getopt

import subprocess
import shlex

import pathlib

filename = "mydocument"
title    = "my title"

output_dir = "output"

author = "Author Name"


ret = 0

def help(options, userdata) :
  print("usage: {0} cmd".format(sys.argv[0]))
  msg = r'''
  cmds
    help
    create
'''

  print(msg)

def all(options, userdata) :
    mclean(options, userdata)
    create(options, userdata)
    add_number(options, userdata)
    change_theme(options, userdata)
    enable_markdown(options, userdata)
    change_docclass(options, userdata)
    add_pages(options, userdata)

def create(options, userdata) :
  cmd = "sphinx-quickstart " + \
    ' -p "{0}"'.format(title) + \
    ' -a "{0}"'.format(author) + \
    ' -v 0.1' + \
    ' -r 1 ' + \
    ' -q' + \
    ' -l "ja"' + \
    ' {0}'.format(output_dir)

  print(cmd)
  subprocess.call(shlex.split(cmd))

def add_number(options, userdata) :
    filepath = output_dir + '/index.rst'
    with open(filepath, mode="rt", encoding="utf-8") as fp:
        lines = fp.read()

    with open(filepath, mode="wt", encoding="utf-8") as fp:
        for line in lines.splitlines() :
            line = re.sub(r'Indices and tables', '索引と表', line)
            line = re.sub(r':maxdepth: 2', ':maxdepth: 6', line)
            fp.write(line + "\n")

            # add numbered after maxdepth
            if re.search(r':maxdepth: 6', line) :
                fp.write('   :numbered:\n')

def change_theme(options, userdata) :
    filepath = output_dir + '/conf.py'
    with open(filepath, mode="rt", encoding="utf-8") as fp:
        lines = fp.read()

    with open(filepath, mode="wt", encoding="utf-8") as fp:
        for line in lines.splitlines() :
            line = re.sub(r"html_theme = 'alabaster'", "html_theme = 'sphinxdoc'", line)
            fp.write(line + "\n")

def enable_markdown(options, userdata) :
    filepath = output_dir + '/conf.py'
    with open(filepath, mode="rt", encoding="utf-8") as fp:
        lines = fp.read()

    with open(filepath, mode="wt", encoding="utf-8") as fp:
        for line in lines.splitlines() :
            line = re.sub(
                "extensions = \[\]",
                "extensions = [ 'myst_parser' ]",
                line)

            fp.write(line + "\n")

def change_docclass(options, userdata) :
    filepath = output_dir + '/conf.py'
    with open(filepath, mode="rt", encoding="utf-8") as fp:
        lines = fp.read()

    with open(filepath, mode="wt", encoding="utf-8") as fp:
        for line in lines.splitlines() :
            fp.write(line + "\n")
        
        fp.write('latex_documents = [\n')
        fp.write('  (\n')
        fp.write("    'index',\n")
        fp.write("    '{0}.tex',\n".format(filename))
        fp.write("    '{0}',\n".format(title))
        fp.write("    '{0}',\n".format(author))
        fp.write("    'manual',\n".format(author))
        fp.write('  )\n')
        fp.write(']\n')

        data = r'''
latex_elements = {
  'papersize' : 'a4paper',
  'classoptions' : ',uplatex,dvipdfmx',
  'extraclassoptions' : 'openany,report,oneside',
  'preamble' : r'\usepackage{mypackage}',
}

latex_docclass = {
  'howto'  : 'jsbook',
  'manual' : 'jsbook',
}

numfig = True

numfig_format = {
  'section' : '%s',
}

source_suffix = {
  '.rst': 'restructuredtext',
  '.txt': 'markdown',
  '.md' : 'markdown',
}
'''

        fp.write(data)

def add_pages(options, userdata) :
    os.makedirs(output_dir + '/pages', exist_ok=True)

    path = pathlib.Path('.')

    exts = [ '*rst', '*.md' ]

    pages = []

    for ext in exts :
        objs = list(path.glob(ext))
        for obj in objs :
            filename = str(obj)
            print(filename)
            src = filename
            dst = output_dir + '/pages/' + filename
            shutil.copy(src, dst)
            pages.append(filename)


    filepath = output_dir + '/index.rst'
    with open(filepath, mode="rt", encoding="utf-8") as fp:
        lines = fp.read()

    with open(filepath, mode="wt", encoding="utf-8") as fp:
        for line in lines.splitlines() :
            fp.write(line + "\n")

            # add pages
            if re.search(r':caption: Contents:', line) :
                fp.write("\n")
                for page in pages :
                    fp.write('   /pages/{0}\n'.format(page))
                



def html(options, userdata) :
  wd = os.getcwd()
  os.chdir(output_dir)

  cmd = "make.bat html"
  print(cmd)
  subprocess.call(shlex.split(cmd))

  os.chdir(wd)

def pdf(options, userdata) :
  os.makedirs(output_dir + '/_build/latex', exist_ok=True)
  shutil.copy("mypackage.sty", output_dir + '/_build/latex/mypackage.sty')

  wd = os.getcwd()
  os.chdir(output_dir)

  cmd = "make.bat latexpdf"
  print(cmd)
  subprocess.call(shlex.split(cmd))

  os.chdir(wd)

def latex(options, userdata) :
  os.makedirs(output_dir + '/_build/latex', exist_ok=True)
  shutil.copy("mypackage.sty", output_dir + '/_build/latex/mypackage.sty')

  wd = os.getcwd()
  os.chdir(output_dir)

  cmd = "make.bat latex"
  print(cmd)
  subprocess.call(shlex.split(cmd))

  os.chdir(wd)

def clean(options, userdata) :
  wd = os.getcwd()
  os.chdir(output_dir)

  cmd = "make.bat clean"
  print(cmd)
  subprocess.call(shlex.split(cmd))

  os.chdir(wd)

def mclean(options, userdata) :
    if os.path.isdir(output_dir) :
        shutil.rmtree(output_dir)

def main():
    ret = 0

    try:
        options, args = getopt.getopt(
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
    
    for o, a in options:
        if o in ("-v", "-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unknown option"
    
    #if output == None :
    #   print("no output option")
    #   ret += 1

    if ret != 0:
        sys.exit(1)
    
    this_function_name = sys._getframe().f_code.co_name

    userdata = {}

    for name in args :
        if name == this_function_name :
            print('WARNING : can not call function recursively')
            continue
        
        if name in globals() :
            func = globals()[name]
            if callable(func) :
                #print('callable')
                func(options, userdata)
            else :
                print('not callable')
        else :
            print("no such function, '{0}'".format(name))
            
    return ret

if __name__ == "__main__" :
    main()


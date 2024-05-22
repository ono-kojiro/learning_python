import random
import re
import sys
from flask import Flask, render_template

from turbo_flask import Turbo
import threading
import time

import json

from MyForm import MyForm

app = Flask(__name__)
turbo = Turbo(app)

app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/toggle')
def toggle():
    return render_template('toggle.html')

@app.route('/myform', methods=['GET', 'POST'])
def myform():
    form = MyForm()
    if form.validate_on_submit():
        val = form.name.data
        return render_template('myform.html', form=form, value=val)
    return render_template('myform.html', form=form)

@app.context_processor
def inject_load():
    if sys.platform.startswith('linux'): 
        with open('/proc/loadavg', 'rt') as f:
            load = f.read().split()[0:3]
    else:
        load = [int(random.random() * 100) / 100 for _ in range(3)]
    return {'load1': load[0], 'load5': load[1], 'load15': load[2]}

@app.context_processor
def inject_hello():
    data = [ "", "", "" ]
    with open('./input.json', 'rt') as f:
        data = json.load(f)
    return {'data0': data[0], 'data1': data[1], 'data2': data[2]}

@app.context_processor
def inject_vmlist():
    data = []
    with open('./vmlist.json', 'rt') as f:
        data = json.load(f)
    return { 'data': data }

#@app.before_first_request
#def before_first_request():
#    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(
                render_template('loadavg.html'), 'load'))
            turbo.push(turbo.replace(
                render_template('hello.html'), 'hello'))
            turbo.push(turbo.replace(
                render_template('vmlist.html'), 'vmlist'))

with app.app_context():
    threading.Thread(target=update_load).start()




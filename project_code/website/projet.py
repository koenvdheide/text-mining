# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:06:28 2017

@author: Rick
"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/results')
def results():
    #retrieve data from database --> post JSON to template
    return render_template("results.html")

@app.route("/sunburst")
def sunburst():
    return render_template("sunburst.html")

@app.route("/tree")
def tree():
    return render_template("tree.html")

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

if __name__ == '__main__':
    app.run()

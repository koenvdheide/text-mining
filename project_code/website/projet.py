import json
from flask import Flask, render_template, request
from flask import Response, jsonify
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

@app.route("/data", methods=['POST', 'GET'])
def get_data():
    print('im here')
    print(str(request.form))
        #table = request.form['table']
        #keyword = request.form['keyword']
        #columns = request.form['columns']
        #keyword_column = request.form['keyword_column']
    return 'x'


if __name__ == '__main__':
    app.run()

import json
from flask import Flask, render_template, request
from flask import Response, jsonify
from SQLConnector import SQLConnector

app = Flask(__name__)
sqlconnection = SQLConnector()

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/results')
def results():
    # retrieve data from database --> post JSON to template
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
    """
    gets called from javascript when user clicks on a sunburst item to fill in the table with relevant information
    :return: the data to be shown in the tables in json format
    """
    table = request.form['table']
    keyword = request.form['keyword']
    columns = request.form['columns']
    keyword_column = request.form['keyword_column']
    if table == 'organism':
        database_data = query_db_join(table, columns, keyword, keyword_column) #to add pubmed ids from article table
    else:
        database_data = query_db(table, columns, keyword, keyword_column)
    return jsonify(table_data=database_data)


def query_db(table, columns, keyword, keyword_column):
    """
    queries the database for the desired entries
    :param table: name of the table to search in
    :param columns: columns to be returned
    :param keyword: keyword to search for
    :param keyword_column: column that must contain the keyword
    :return: first hit in a list format
    """
    rows = sqlconnection.text_select(table, columns, keyword_column, keyword)
    for row in rows:
        return list(row)

# identical to above except that a join with the article table is also performed
def query_db_join(table, columns, keyword, keyword_column):
    """
    queries the database for the desired entries
    :param table: name of the table to search in
    :param columns: columns to be returned
    :param keyword: keyword to search for
    :param keyword_column: column that must contain the keyword
    :return: first hit in a list format
    """
    rows = sqlconnection.text_select_join(table, columns, keyword_column, keyword)
    for row in rows:
        return list(row)

if __name__ == '__main__':
    app.run()

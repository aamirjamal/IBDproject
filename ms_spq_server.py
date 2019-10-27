import pypyodbc as pypyodbc
from flask import Flask, request
from flask import render_template


app = Flask(_name_)
cnxnStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-105P9O9\SQLEXPRESS;DATABASE=Test;Trusted_Connection=yes;'


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/query1.html', methods=['GET', 'POST'])
def query1():
    return render_template('query1.html')


@app.route('/q1', methods=['GET', 'POST'])
def q1():
    if request.method == "GET":
        details = request.args
        name = details['name']
        reviews = details['reviews']
        cnxn = pypyodbc.connect(cnxnStr)
        cur = cnxn.cursor()
        cur.execute("Enter query 1 here")
        data = cur.fetchall()
        return render_template("q1table.html", data=data)


@app.route('/q2', methods=['GET', 'POST'])
def q2():
    if request.method == "GET":
        details = request.args
        btype = details['type']
        bzip = details['zip']
        percent = details['percent']
        rating = details['rating']
        cnxn = pypyodbc.connect(cnxnStr)
        cur = cnxn.cursor()
        cur.execute("Enter query 2 here")
        data = cur.fetchall()
        return render_template("q2table.html", data=[btype, bzip, percent, rating])


@app.route('/q3', methods=['GET', 'POST'])
def q3():
    if request.method == "GET":
        details = request.args
        btype = details['type']
        bzip = details['zip']
        start = details['startdate']
        end = details['enddate']
        cnxn = pypyodbc.connect(cnxnStr)
        cur = cnxn.cursor()
        cur.execute("Enter query 3 here")
        data = cur.fetchall()
        return render_template("q3table.html", data=[btype, bzip, start, end])


@app.route('/q4', methods=['GET', 'POST'])
def q4():
    if request.method == "GET":
        details = request.args
        key = details['userid']
        cnxn = pypyodbc.connect(cnxnStr)
        cur = cnxn.cursor()
        cur.execute("Enter query 4 here")
        data = cur.fetchall()
        return render_template("q4table.html", data=[key])


@app.route('/q5', methods=['GET', 'POST'])
def q5():
    if request.method == "GET":
        details = request.args
        rname = details['resName']
        cnxn = pypyodbc.connect(cnxnStr)
        cur = cnxn.cursor()
        cur.execute("Enter query 5 here")
        data = cur.fetchall()
        return render_template("q5table.html", data=[rname])


@app.route('/query2.html', methods=['GET', 'POST'])
def query2():
    return render_template('query2.html')


@app.route('/query3.html', methods=['GET', 'POST'])
def query3():
    return render_template('query3.html')


@app.route('/query4.html', methods=['GET', 'POST'])
def query4():
    return render_template('query4.html')


@app.route('/query5.html', methods=['GET', 'POST'])
def query5():
    return render_template('query5.html')


if _name_ == '_main_':
    app.run(debug=True)

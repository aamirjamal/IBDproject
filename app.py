from flask import Flask, request
from flask import render_template
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = '129.21.65.218'
app.config['MYSQL_USER'] = 'aj'
app.config['MYSQL_PASSWORD'] = 'abcd1234'
app.config['MYSQL_DB'] = 'MyDatabaseFinal'
app.config['MYSQL_CONNECT_TIMEOUT'] = 180

mysql = MySQL(app)


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
        cur = mysql.connection.cursor()
        cur.execute("""select name from user_table 
                    where name like '{0}%' and user_id in 
                    (select u_id from reviewTable 
                    group by u_id 
                    having count(u_id) > {1});"""
                    .format(name, reviews))
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

        # cur = mysql.connection.cursor()
        # cur.execute("""select name from business_table2 where postal_code ='{zip}' and business_id in (select b_id from reviewTable group by b_id having avg(b_id)>{rating});""")
        # data = cur.fetchall()
        return render_template("q2table.html", data=[btype, bzip, percent, rating])


@app.route('/q3', methods=['GET', 'POST'])
def q3():
    if request.method == "GET":
        details = request.args
        btype = details['type']
        bzip = details['zip']
        start = details['startdate']
        end = details['enddate']

        # cur = mysql.connection.cursor()
        # cur.execute("""select name from business_table2 where postal_code ='{zip}' and business_id in (select b_id from reviewTable group by b_id having avg(b_id)>{rating});""")
        # data = cur.fetchall()
        return render_template("q3table.html", data=[btype, bzip, start, end])


@app.route('/q4', methods=['GET', 'POST'])
def q4():
    if request.method == "GET":
        details = request.args
        key = details['userid']

        # cur = mysql.connection.cursor()
        # cur.execute("""select name from business_table2 where postal_code ='{zip}' and business_id in (select b_id from reviewTable group by b_id having avg(b_id)>{rating});""")
        # data = cur.fetchall()
        return render_template("q4table.html", data=[key])


@app.route('/q5', methods=['GET', 'POST'])
def q5():
    if request.method == "GET":
        details = request.args
        rname = details['resName']

        # cur = mysql.connection.cursor()
        # cur.execute("""select name from business_table2 where postal_code ='{zip}' and business_id in (select b_id from reviewTable group by b_id having avg(b_id)>{rating});""")
        # data = cur.fetchall()
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


@app.route('/sel_usr', methods=['GET', 'POST'])
def sel_usr():
    return render_template('select_user.html')


@app.route('/sel_usr_table', methods=['GET', 'POST'])
def usr_table():
    if request.method == "GET":
        details = request.args
        name = details['name']
        min_rating = details['min']
        max_rating = details['max']

        cur = mysql.connection.cursor()
        cur.execute(
            """select name from user_table where name ='{0}' and average_stars >= {1} and average_stars <= {2}""".format(name, min_rating, max_rating))
        data = cur.fetchall()
        return render_template("sel_usr_table.html", data=[data])


if __name__ == '__main__':
    app.run(debug=True)

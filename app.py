from flask import Flask, request
from flask import render_template
import pypyodbc


app = Flask(__name__)

cnxnStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-3BKTPOD;DATABASE=yelp;Trusted_Connection=yes;'







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
        # cur = mysql.connection.cursor()
        # cur.execute("""select name from user_table
        #             where name like '{0}%' and user_id in
        #             (select u_id from reviewTable
        #             group by u_id
        #             having count(u_id) > {1});"""
        #             .format(name, reviews))

        cnxn = pypyodbc.connect(cnxnStr)
        cur = cnxn.cursor()
        cur.execute("""select name from userTable where name like '{0}%' and u_id in (select u_id from reviewTable group by u_id having count(u_id) > {1});"""
                     .format(name, reviews))
        data = cur.fetchall()
        return render_template("q1table.html", data=data)


@app.route('/q2', methods=['GET', 'POST'])
def q2():
    if request.method == "GET":
        details = request.args
        btype = details['type']
        bzip = details['zip']
        percent = int(details['percent'])/100
        rating = details['rating']

        # cur = mysql.connection.cursor()
        # cur.execute("""select name from business_table2 where postal_code ='{zip}' and business_id in (select b_id from reviewTable group by b_id having avg(b_id)>{rating});""")

        cnxn = pypyodbc.connect(cnxnStr)
        cur = cnxn.cursor()
        cur.execute(
            """SELECT tab1.name from  ( SELECT b1.name, b1.business_id ,count(rev1.r_id) as count1 from businessTable as b1 join {0} as r1 on b1.business_id = r1.business_id join reviewTable as rev1 on b1.business_id = rev1.b_id where b1.postal_code='{1}' group by b1.business_id,b1.name) as tab1

join

( SELECT b2.name, b2.business_id ,count(rev2.r_id) as count2 from businessTable as b2 join {0} as r2 on b2.business_id = r2.business_id join reviewTable as rev2 on b2.business_id = rev2.b_id where b2.postal_code='{1}' and rev2.stars>{3} group by b2.business_id,b2.name) as tab2

ON tab1.business_id=tab2.business_id WHERE count2/count1 >{2};"""
            .format(btype,bzip,percent,rating))
        data = cur.fetchall()
        return render_template("q2table.html", data=data)


@app.route('/q3', methods=['GET', 'POST'])
def q3():
    if request.method == "GET":
        details = request.args
        btype = details['type']
        bzip = details['zip']
        start = details['startdate']
        end = details['enddate']

        cur = pypyodbc.connection.cursor()
        cur.execute("""SELECT businessTable.name from businessTable join {0} on businessTable.business_id = {0}.business_id join checkinTable on businessTable.business_id = checkinTable.b_id where businessTable.postal_code='{1}' and CONVERT(datetime,checkinTable.date) between CAST('{2}' as date) and CAST('{3}}' as date) group by businessTable.business_id,businessTable.name order by sum(checkinTable.occurence) DESC;
;""".format(btype,bzip,start,end))
        data = cur.fetchall()
        return render_template("q3table.html", data=data)


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

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
            .format(btype, bzip, percent, rating))
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

        cnxn = pypyodbc.connect(cnxnStr)
        cur = cnxn.cursor()
        cur.execute(
            """SELECT businessTable.name from businessTable join {0} on businessTable.business_id = {0}.business_id join checkinTable on businessTable.business_id = checkinTable.b_id where businessTable.postal_code='{1}' and CONVERT(datetime,checkinTable.date) between CAST('2016-01-01' as date) and CAST('2017-01-01' as date) group by businessTable.business_id,businessTable.name order by sum(checkinTable.occurence) DESC;"""
            .format(btype, bzip, start, end))
        data = cur.fetchall()
        return render_template("q3table.html", data=data)


@app.route('/q4', methods=['GET', 'POST'])
def q4():
    if request.method == "GET":
        details = request.args
        key = details['userid']

        cnxn = pypyodbc.connect(cnxnStr)
        cur = cnxn.cursor()
        cur.execute(
            """SELECT tab1.name from

(SELECT b1.name, b1.business_id,count(rev1.r_id) as count1 from friendsTable as f1 join userTable as u1 on f1.u_id=u1.u_id join reviewTable as rev1 on f_id=rev1.u_id join businessTable as b1 on rev1.b_id=b1.business_id join restaurantTable as r1 on b1.business_id=r1.business_id where rev1.stars>4  and u1.u_id='{0}' group by b1.business_id,b1.name) as tab1

join

(SELECT b2.name,b2.business_id,count(rev2.r_id) as count2 from friendsTable as f2 join userTable u2 on f2.u_id=u2.u_id join reviewTable as rev2 on f_id=rev2.u_id join businessTable as b2 on rev2.b_id=b2.business_id join restaurantTable as r2 on b2.business_id=r2.business_id where rev2.stars<3 and u2.u_id='{0}'  group by b2.business_id,b2.name) as tab2

ON tab1.business_id=tab2.business_id WHERE count1>count2 ;;"""
                .format(key))
        data = cur.fetchall()
        return render_template("q4table.html", data=data)


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


# business review query here.. pls delete this comment after writing the query..
@app.route('/sel_usr_table', methods=['GET', 'POST'])
def usr_table():
    if request.method == "GET":
        details = request.args
        name = details['name']
        b_zip = details['zip']

        cnxn = pypyodbc.connect(cnxnStr)
        cur = cnxn.cursor()
        # query should return reviewer name, review text and stars.
        cur.execute("""SELECT userTable.name,reviewTable.text,reviewTable.stars FROM businessTable join reviewTable on businessTable.business_id=reviewTable.b_id join userTable on reviewTable.u_id=userTable.u_id where businessTable.name='{0}' and businessTable.postal_code='{1}' ;""".format(name, b_zip))
        data = cur.fetchall()
        return render_template("sel_usr_table.html", data=[data])


@app.route('/find_b', methods=['GET', 'POST'])
def find_business():
    return render_template('find_business.html')


@app.route('/find_b_table', methods=['GET', 'POST'])
def find_business_table():
    if request.method == "GET":
        details = request.args
        b_type = details['type']
        b_zip = details['zip']
        stars = details['stars']
        cnxn = pypyodbc.connect(cnxnStr)
        cur = cnxn.cursor()
        # query should return business name, business address and desc stars.
        cur.execute("""select query for """.format(b_type, b_zip, stars))
        data = cur.fetchall()
        return render_template("find_b_table.html", data=[data])


if __name__ == '__main__':
    app.run(debug=True)

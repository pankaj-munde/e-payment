from flask import Flask, render_template, redirect, url_for, request
import sqlite3
from sqlite3 import Error
from flask import jsonify
import time
import GT_521F52


app = Flask('__name__')
database = 'user_database.db'


@app.route('/background_process')
def background_process():

    try:
        p = GT_521F52.PyFingerprint_GT_521F52('/dev/ttyUSB0')

    except Exception as e:
        print("Something went wrong")
        print('Exception message: ' + str(e))

    try:
        print("Put your finger three times at the scanner to enrrol")
        fid = p.enrollUser()
        print('Enrolled Id : {}'.format(fid))
        return jsonify(result='Fingerprint Enrolled Successfully!!!', fid=str(fid))
    except Exception as e:
        return jsonify(result='Failed...Try Again!!!', fid="None")
        print('Exception message: ' + str(e))


def delete_fingerprint(fid):
    """Deletes fingerprint from sensor's memory"""
    try:
        p = GT_521F52.PyFingerprint_GT_521F52('/dev/ttyUSB0')

    except Exception as e:
        print("Something went wrong")
        print('Exception message: ' + str(e))


    try:

        p.delete(fid)
        print('Fingerprint of id : {0} deleted successfully'.format(fid))
    except Exception as e:
        print('Exception message: ' + str(e))


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def insertUser(con, username, name, addr, phn_num, bal, fid):
    # con = create_connection("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO user_info (username,name,addr,phone_num,bal,fid) VALUES (?,?,?,?,?,?)",
                (username, name, addr, phn_num, bal, fid))
    con.commit()
    con.close()

def _get_fid(conn, mail):
    cur = conn.cursor()
    sql_qry = """SELECT * FROM user_info where username = ?"""
    cur.execute(sql_qry, (mail,))
    users = cur.fetchall()
    fid = users[0][-1]
    return fid


def delete_user(conn, username):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM user_info WHERE username=?'
    fid = _get_fid(conn, username)
    time.sleep(0.1)
    cur = conn.cursor()
    cur.execute(sql, (username,))
    conn.commit()
    conn.close()
    ## Also delete user fingerprint
    delete_fingerprint(fid)

def retrieveUsers():
    con = create_connection("user_database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM user_info")
    users = cur.fetchall()
    con.close()
    return users


# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print('username = {0} password={1}'.format(username, password))
        if username == 'snehal' and password == '1234':
            return redirect(url_for('index'))
        else:
            return render_template('login_fail.html')
    return render_template('home.html')


@app.route('/index', methods=["GET", "POST"])
def index():
    user_info = retrieveUsers()
    print(user_info)
    # Add user to DB
    # parser = AdvancedHTMLParser.AdvancedHTMLParser()
    # parser.parseFile('templates/index.html')
    # ele_id = parser.getElementById('fscan')
    # print(ele_id)

    # print('Got id = {}'.format(ele_id))
    if request.method == 'POST':
        if request.form['submit_button'] == 'Add':

            add_name = request.form['add_name']
            add_email = request.form['add_email']
            add_addr = request.form['add_addr']
            add_phn = request.form['add_phn']
            add_bal = request.form['add_bal']
            fid = request.form['fid']
            # create a database connection
            conn = create_connection(database)

            # create tables
            if conn is not None:
                # create user
                insertUser(conn, add_email,add_name, add_addr, add_phn, add_bal, fid)
                print('[Info]| Operation Successfull')
                return redirect(url_for('index'))

        if request.form['submit_button'] == 'Delete':

            edt_email = request.form['del_email']
            print('edt_email : ', edt_email)
            # create a database connection
            conn = create_connection(database)

            # create tables
            if conn is not None:
                # create user
                delete_user(conn, edt_email)
                print('[Info]| Operation Successfull')
                return redirect(url_for('index'))

            delete_fingerprint()
    return render_template('index.html', users=user_info)


@app.route('/add_user', methods=["POST"])
def edit_user():
    pass


# @app.route('/login_check', methods=['GET', 'POST'])
# def check_login():
#     print((request.form['username'], request.form['password']))
#     return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

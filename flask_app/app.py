
from flask import Flask, render_template, redirect, url_for, request
import sqlite3
from sqlite3 import Error

app = Flask('__name__')
database = 'user_database.db'



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


def insertUser(con,username,password,name,addr,phn_num,bal):
    # con = create_connection("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO user_info (username,password,name,addr,phone_num,bal) VALUES (?,?,?,?,?,?)", (username,password,name,addr,phn_num,bal))
    con.commit()
    con.close()


def delete_user(conn, username):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM user_info WHERE username=?'
    cur = conn.cursor()
    cur.execute(sql, (username,))
    conn.commit()


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
    if request.method=='POST':
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
    # Add user to DB
    if request.method =='POST':
        if request.form['submit_button'] == 'Add':
                
            add_name = request.form['add_name']
            add_email = request.form['add_email']
            add_addr = request.form['add_addr']
            add_phn = request.form['add_phn']
            add_bal = request.form['add_bal']
            # create a database connection
            conn = create_connection(database)

            # create tables
            if conn is not None:
                # create user
                insertUser(conn, add_email, "1234", add_name, add_addr, add_phn, add_bal)
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
        # return render_template('index.html', users = user_info)
    return render_template('index.html', users = user_info)
    
    
@app.route('/add_user', methods=["POST"])
def edit_user():
    pass
    
    
# @app.route('/login_check', methods=['GET', 'POST'])
# def check_login():
#     print((request.form['username'], request.form['password']))
#     return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
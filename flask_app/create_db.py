import sqlite3
from sqlite3 import Error
import time

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("DB Connection Established Successfully")
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insertUser(con, username,password,name,addr,phn_num,bal):
    # con = create_connection("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO user_info (username,password,name,addr,phone_num,bal) VALUES (?,?,?,?,?,?)", (username,password,name,addr,phn_num,bal))
    con.commit()
    con.close()

def retrieveUsers():
    con = create_connection("user_database.db")
    cur = con.cursor()
    sql_qry = """SELECT * FROM user_info where fid = ?"""
    cur.execute(sql_qry, ('1',))
    users = cur.fetchall()
    con.close()
    return users

def update_db():
    con = create_connection('user_database.db')
    cursor = con.cursor()

    sql_update_query = """Update user_info set bal = ? where fid = ?"""
    data = ("200", '1')
    cursor.execute(sql_update_query, data)
    con.commit()
    print("Record Updated successfully")
    cursor.close()

def main():
    database = r"user_database.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS user_info (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        username text NOT NULL,
                                        name text NOT NULL,
                                        addr text NOT NULL,
                                        phone_num text NOT NULL,
                                        bal integer NOT NULL,
                                        fid integer NOT Null
                                    ); """


    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        # create_table(conn, sql_create_projects_table)
        # create user
        # insertUser(conn, 'pankaj.pan@gmail.com',"1234","Pankaj Pandhare", "Pune","7387421143", 100)
        # update_db()
        # time.sleep(0.2)
        user = retrieveUsers()
        
        print(user[0][-2])
        print('[Info]| Operation Successfull')
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
from mysql.connector import errorcode
import mysql.connector

def setup_db_connection(user, password, host, database):
    try:
        return mysql.connector.connect(user=user, password=password, host=host, database=database)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not")
        else:
            print("Something is wrong with your user name or")
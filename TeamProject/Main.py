#!/usr/bin/env python
import config as cfg
import mysql.connector
from mysql.connector import errorcode

def setup_db_connection(user, password, host, database):
    try:
        return mysql.connector.connect(user=user, password=password, host=host, database=database)

    except mysql.connector as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not")
        else:
            print("Something is wrong with your user name or")


db_conn = setup_db_connection(cfg.mysql["user"], cfg.mysql["password"], cfg.mysql["host"], cfg.mysql["db"])

print("welcome to " + db_conn.get_server_info())


db_conn.close()
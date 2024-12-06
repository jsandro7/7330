from mysql.connector import errorcode
import mysql.connector
from TeamProject.Utilities import Config as cfg
from nicegui import ui

def setup_db_connection(user, password, host, database):
    try:
        return mysql.connector.connect(user=user, password=password, host=host, database=database)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            ui.notify("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            ui.notify("Database does not")
        else:
            ui.notify("Something is wrong with your user name or")


def create_conn():
    conn = setup_db_connection(cfg.mysql["user"], cfg.mysql["password"], cfg.mysql["host"], cfg.mysql["db"])

    return conn
from nicegui import ui

import Degree
import Config as cfg
import MySql
import Menu


@ui.page('/')
def index_page() -> None:
    db_conn = MySql.setup_db_connection(cfg.mysql["user"], cfg.mysql["password"], cfg.mysql["host"], cfg.mysql["db"])

    Menu.menu()
    Degree.page(db_conn)

    db_conn.close()
ui.run(title="Degree Evaluator")


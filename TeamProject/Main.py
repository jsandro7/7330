from nicegui import ui

from TeamProject.Utilities import Config as cfg, MySql
import Menu
from TeamProject.Pages import Course, Degree, Section, Instructor, Goal

def create_conn():
    return MySql.setup_db_connection(cfg.mysql["user"], cfg.mysql["password"], cfg.mysql["host"], cfg.mysql["db"])


@ui.page('/')
def index_page() -> None:
    db_conn = create_conn()
    Menu.create_menu()
    Degree.page(db_conn)
    db_conn.close()

@ui.page('/course')
def index_page() -> None:
    db_conn = create_conn()
    Menu.create_menu()
    Course.page(db_conn)
    db_conn.close()

@ui.page('/section')
def index_page() -> None:
    db_conn = create_conn()
    Menu.create_menu()
    Section.page(db_conn)
    db_conn.close()

@ui.page('/instructor')
def index_page() -> None:
    db_conn = create_conn()
    Menu.create_menu()
    Instructor.page(db_conn)
    db_conn.close()

@ui.page('/goal')
def index_page() -> None:
    db_conn = create_conn()
    Menu.create_menu()
    Goal.page(db_conn)
    db_conn.close()

ui.run(title="Degree Evaluator")

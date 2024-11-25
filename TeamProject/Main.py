import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nicegui import ui
import Menu
from TeamProject.Pages import Course, Degree, Section, Instructor, Goal

@ui.page('/')
def index_page() -> None:
    Menu.create_menu()
    Degree.page()

@ui.page('/course')
def index_page() -> None:
    Menu.create_menu()
    Course.page()

@ui.page('/section')
def index_page() -> None:
    Menu.create_menu()
    Section.page()

@ui.page('/instructor')
def index_page() -> None:
    Menu.create_menu()
    Instructor.page()

@ui.page('/goal')
def index_page() -> None:
    Menu.create_menu()
    Goal.page()

ui.run(title="Degree Evaluator")

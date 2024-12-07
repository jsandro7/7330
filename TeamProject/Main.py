import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nicegui import ui, app
import Menu
from TeamProject.Pages import Course, Degree, Instructor, Goal

app.on_exception(ui.notify)

@ui.page('/')
def index_page() -> None:
    Menu.create_menu('Current Degrees')
    Degree.page()

@ui.page('/course')
def index_page() -> None:
    Menu.create_menu('Current Courses')
    Course.page()

@ui.page('/instructor')
def index_page() -> None:
    Menu.create_menu('Current Instructors')
    Instructor.page()

@ui.page('/goal')
def index_page() -> None:
    Menu.create_menu('Current Goals')
    Goal.page()

ui.run(title="Degree Evaluator")

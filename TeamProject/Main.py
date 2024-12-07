import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nicegui import ui, app
import Menu
from TeamProject.Pages import Course, CourseReport, Degree, DegreeReport, Home, Evaluations, EvaluationsReport, Instructor, InstructorReport, Goal


app.add_static_file(local_file='Logo.png', url_path='/logo.png')

app.on_exception(ui.notify)

@ui.page('/')
def index_page() -> None:
    Menu.create_menu('Home Page')
    Home.page()

@ui.page('/degree')
def index_page() -> None:
    Menu.create_menu('Current Degrees')
    Degree.page()

@ui.page('/degree_report')
def index_page() -> None:
    Menu.create_menu('Degrees')
    DegreeReport.page()

@ui.page('/course')
def index_page() -> None:
    Menu.create_menu('Current Courses')
    Course.page()

@ui.page('/course_report')
def index_page() -> None:
    Menu.create_menu('Courses')
    CourseReport.page()   

@ui.page('/instructor')
def index_page() -> None:
    Menu.create_menu('Current Instructors')
    Instructor.page()

@ui.page('/instructor_report')
def index_page() -> None:
    Menu.create_menu('Instructors')
    InstructorReport.page()

@ui.page('/goal')
def index_page() -> None:
    Menu.create_menu('Current Goals')
    Goal.page()

@ui.page('/evaluations')
def index_page() -> None:
    Menu.create_menu('Evaluations')
    Evaluations.page()

@ui.page('/evaluations_report')
def index_page() -> None:
    Menu.create_menu('Evaluations Report')
    EvaluationsReport.page()
    

ui.run(title="Degree Evaluator")
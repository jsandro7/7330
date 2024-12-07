from nicegui import ui

def create_menu(site_name) -> None:
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label(site_name.upper())
        with ui.button(icon='menu'):
            with ui.menu().props('auto-close').style('width:150px'):
                ui.menu_item("Degree", lambda:  ui.navigate.to("/"))
                ui.menu_item("Degree Report", lambda:  ui.navigate.to("/degree_report"))
                ui.menu_item("Course", lambda: ui.navigate.to("/course"))
                ui.menu_item("Course Report", lambda: ui.navigate.to("/course_report"))
                ui.menu_item("Instructor", lambda: ui.navigate.to("/instructor"))
                ui.menu_item("Instructor Report", lambda: ui.navigate.to("/instructor_report"))
                ui.menu_item("Goals", lambda: ui.navigate.to("/goal"))
                ui.menu_item("Evaluations", lambda: ui.navigate.to("/evaluations"))
                ui.menu_item("Evaluations Report", lambda: ui.navigate.to("/evaluations_report"))
    with ui.footer().style('background-color: #3874c8').classes('justify-between'):
        ui.label('DEGREE EVALUATOR')
        ui.label('Copyright © SMU 2024')
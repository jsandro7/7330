from nicegui import ui

def create_menu(site_name) -> None:
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label(site_name.upper())
        with ui.button(icon='menu'):
            with ui.menu().props('auto-close'):
                ui.menu_item("Degree", lambda:  ui.navigate.to("/"))
                ui.menu_item("Course", lambda: ui.navigate.to("/course"))
                ui.menu_item("Instructor", lambda: ui.navigate.to("/instructor"))
                ui.menu_item("Goals", lambda: ui.navigate.to("/goal"))
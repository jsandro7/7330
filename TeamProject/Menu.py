from nicegui import ui

def create_menu() -> None:
    with ui.row().classes('w-full items-center'):
        result = ui.label().classes('mr-auto')
        with ui.button(icon='menu'):
            with ui.menu().props('auto-close'):
                ui.menu_item("Home", lambda:  ui.navigate.to("/"))
                ui.menu_item("Course", lambda: ui.navigate.to("/course"))
                ui.menu_item("Section", lambda: ui.navigate.to("/section"))
                ui.menu_item("Instructor", lambda: ui.navigate.to("/instructor"))
                ui.menu_item("Goals", lambda: ui.navigate.to("/goal"))


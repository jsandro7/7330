from nicegui import ui

def menu() -> None:
    ui.link('Home', '/').classes(replace='text-blue')
    ui.link('Course', '/course').classes(replace='text-blue')
    ui.link('Instructor', '/instructor').classes(replace='text-blue')
    ui.link('Section', '/section').classes(replace='text-blue')
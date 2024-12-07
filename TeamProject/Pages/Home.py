from nicegui import ui



def page():
    with ui.element('div').classes('columns-2 w-full gap-2'):
        
        with ui.column():
            ui.label('Welcome to the Degree Evalutor').style('font-size:25px; font-weight:bold; color:navy;')
            ui.image('logo.png').style('width:500px')
        
        with ui.column():
            ui.label('Data Entry').style('font-size:25px; font-weight:bold; color:navy;')
            with ui.list().props('dense separator'):
                ui.item('Course').on_click(lambda:  ui.navigate.to("/course"))
                ui.item('Degree').on_click(lambda:  ui.navigate.to("/degree"))               
                ui.item('Evaluation').on_click(lambda:  ui.navigate.to("/evaluations"))
                ui.item('Goal').on_click(lambda:  ui.navigate.to("/evaluations"))
                ui.item('Instructor').on_click(lambda:  ui.navigate.to("/instructor"))
            ui.label('Reports').style('font-size:25px; font-weight:bold; color:navy;')
            with ui.list().props('dense separator'):
                ui.item('Courses').on_click(lambda:  ui.navigate.to("/course_report"))
                ui.item('Degrees').on_click(lambda:  ui.navigate.to("/degree_report"))               
                ui.item('Evaluations').on_click(lambda:  ui.navigate.to("/evaluations_report"))
                ui.item('Instructor').on_click(lambda:  ui.navigate.to("/instructor_report"))   
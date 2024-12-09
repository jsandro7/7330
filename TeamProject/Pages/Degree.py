from nicegui import ui
from TeamProject.Utilities import MySql, Validation

def get_degrees():
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        name,
        level
    FROM degree    
    """
    cursor.execute(stmt)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_degrees_courses(args):
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT 
        c.course_id,
        c.name,
        dc.is_core
    FROM degree d
    JOIN degree_course dc ON d.name = dc.name AND d.level = dc.level
    JOIN course c ON c.course_id = dc.course_id  
    WHERE d.name = %s AND d.level = %s
    """
    cursor.execute(stmt, args)
    rows = cursor.fetchall()
    conn.close()

    return rows


def insert_degree(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO degree
    (
        name,
        level
    )
    VALUES (%s, %s)    
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def insert_degree_course(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO degree_course
    (
        course_id,
        is_core,
        name,
        level            
    )
    VALUES (%s, %s, %s, %s)    
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()


def delete_degree(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    DELETE FROM degree
    WHERE name = %s AND level = %s 
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def update_degree_course(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    UPDATE degree_course
    SET is_core = %s
    WHERE course_id = %s AND name = %s AND level = %s
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def delete_degree_course(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    DELETE FROM degree_course
    WHERE name = %s AND level = %s AND course_id = %s
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def handle_save(ui, dialog, inputs):
    if Validation.check_entries(ui, inputs):
        dialog.submit([field.value for field in inputs.values()])

def page():

    rows = get_degrees()

    columns = [
        {'field': 'name', 'editable': False, 'sortable': True},
        {'field': 'level', 'editable': False, 'sortable': True},
    ]

    columnsCourse = [
        {'field': 'course_id', 'editable': False, 'sortable': True},
        {'field': 'name', 'editable': False, 'sortable': True},
        {'field': 'is_core', 'editable': True, 'sortable': True},
    ]

    rowsCourse = []

    #Event Handlers

    async def add_row():
        with ui.dialog() as dialog, ui.card():
            inputs = {
                'Degree Name': ui.input(label='Type Degree Name'),
                'Degree Level': ui.input(label='Type Degree Level')                
            }
            # Save and Cancel buttons
            with ui.row():
                ui.button(
                    'Save',
                    on_click=lambda: handle_save(ui, dialog, inputs)
                )
                ui.button('Cancel', on_click=lambda: dialog.close())


        result = await dialog
        if(result is None):
            return
        insert_degree(result)

        ui.notify(f'Degree added', color="positive")

        rows.clear()
        rows.extend(get_degrees())
        aggrid.update()

    async def handle_row_select_change(e):
        selected = [row for row in await aggrid.get_selected_rows()][0]

        result = get_degrees_courses([selected['name'], selected['level']])

        rowsCourse.clear()
        rowsCourse.extend(result)
        aggridCourse.update()

    async def delete_selected():
        selected = [row for row in await aggrid.get_selected_rows()][0]

        delete_degree([selected['name'], selected['level']])

        ui.notify(f'Deleted degree name {selected["name"]}, level {selected["level"]}', color="positive")

        rows.clear()
        rows.extend(get_degrees())
        aggrid.update()

    async def add_course(r):
        with ui.dialog() as dialog, ui.card():
            inputs = {
                'Course ID': ui.input(label='Type Course ID'),
                'Is Core': ui.input(label='Core Course?')
            }
            # Save and Cancel buttons
            with ui.row():
                ui.button(
                    'Save',
                    on_click=lambda: handle_save(ui, dialog, inputs)
                )
                ui.button('Cancel', on_click=lambda: dialog.close())


        result = await dialog

       

        if(not result):
            return
        
        is_core = int(result.pop())
        selectedDegree = [row for row in await aggrid.get_selected_rows()][0]
        result.extend([is_core, selectedDegree['name'], selectedDegree['level']])

        insert_degree_course(result)

        ui.notify(f'Course added', color="positive")

        rowsCourse.clear()
        rowsCourse.extend(get_degrees_courses([selectedDegree['name'], selectedDegree['level']]))
        aggridCourse.update()

    async def deleteCourse_selected():
        selected = [row for row in await aggridCourse.get_selected_rows()][0]
        selectedDegree = [row for row in await aggrid.get_selected_rows()][0]

        delete_degree_course([selectedDegree['name'], selectedDegree['level'], selected['course_id']])    

        ui.notify(f'Deleted course with ID {selected["course_id"]}', color="positive")    

        rowsCourse.clear()
        rowsCourse.extend(get_degrees_courses([selectedDegree['name'], selectedDegree['level']]))
        aggridCourse.update()


    async def update_is_core_change(e):
        row = e.args["data"]
        selectedDegree = [row for row in await aggrid.get_selected_rows()][0]
        
        newVal = e.args['newValue']
        update_degree_course([newVal, row['course_id'], selectedDegree['name'], selectedDegree['level']])
        ui.notify(f'Updated degree course Is Core: {newVal}', color="positive")

        rowsCourse.clear()
        rowsCourse.extend(get_degrees_courses([selectedDegree['name'], selectedDegree['level']]))
        aggridCourse.update()

    #Form Elements
    with ui.row().classes('items-left'):
        ui.button('Remove Degree', on_click=delete_selected)
        ui.button('New Degree', on_click=add_row)

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'single',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('rowSelected', handle_row_select_change)


    with ui.row().classes('items-left'):
        ui.button('Remove Course From Degree', on_click=deleteCourse_selected)
        ui.button('Assign Course To Degree', on_click=add_course)

    aggridCourse = ui.aggrid({
        'columnDefs': columnsCourse,
        'rowData': rowsCourse,
        'rowSelection': 'single',
        'stopEditingWhenCellsLoseFocus': True,
    }).on("cellValueChanged", update_is_core_change)


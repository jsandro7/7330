from nicegui import ui
from TeamProject.Utilities import MySql, Validation

def get_course():
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        course_id,
        name
    FROM course    
    """

    cursor.execute(stmt)
    rows = cursor.fetchall()
    conn.close()

    return rows

def get_course_sections(args):
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT 
        c.course_id,
        c.name
    FROM section s
    JOIN course c ON c.course_id = s.course_id
    WHERE c.course_id = %s
    """

    cursor.execute(stmt, args)
    rows = cursor.fetchall()

    conn.close()

    return rows

def insert_course(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO course
    (
        course_id,
        name
    )
    VALUES (%s, %s)    
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def delete_course(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    DELETE FROM course
    WHERE course_id = %s
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def handle_save(ui, dialog, inputs):
    if Validation.check_entries(ui, inputs):
        dialog.submit([field.value for field in inputs.values()])

def page():

    rows = get_course()

    columns = [
        {'field': 'course_id', 'editable': False, },
        {'field': 'name', 'editable': True, 'sortable': True},
    ]

    async def add_row():
        with ui.dialog() as dialog, ui.card():
            inputs = {
                'Course ID': ui.input(label='Type Course ID'),
                'Course Name': ui.input(label='Type Course Name')
            }
            # Save and Cancel buttons
            with ui.row():
                ui.button(
                    'Save',
                    on_click=lambda: handle_save(ui, dialog, inputs)
                )
                ui.button('Cancel', on_click=lambda: dialog.close())


        result = await dialog
        insert_course(result)

        rows.clear()
        rows.extend(get_course())
        aggrid.update()

    async def handle_row_select_change(e):
        selected = [row for row in await aggrid.get_selected_rows()][0]

        result = get_course_sections([selected['course_id']])

        rows.clear()
        rows.extend(result)
        rows.update()
    
    async def delete_selected():
        selected = [row for row in await aggrid.get_selected_rows()][0]

        delete_course([selected['course_id']])

        ui.notify(f'Deleted course with ID {selected["course_id"]}')

        rows.clear()
        rows.extend(get_course())
        aggrid.update()

    with ui.row().classes('items-left'):
        ui.button('Remove Course', on_click=delete_selected)
        ui.button('New Course', on_click=add_row)

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_row_select_change)
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
    if Validation.check_entries(inputs):
        dialog.submit([input_widget.value for input_widget in inputs.values()])
    else:
        ui.notify("Please fix errors before saving.", color="red")

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
                    on_click=handle_save(ui, dialog, inputs)
                )
                ui.button('Cancel', on_click=lambda: dialog.close())


        result = await dialog
        insert_course(result)

        rows.clear()
        rows.extend(get_course())
        aggrid.update()

    async def handle_row_select_change(e):
        selected = [row for row in await aggrid.get_selected_rows()][0]

        result = get_course([selected['course_id'], selected['name']])

        rows.clear()
        rows.extend(result)
        rows.update()

    async def delete_selected():
        selected_id = [row['id'] for row in await aggrid.get_selected_rows()]
        rows[:] = [row for row in rows if row['id'] not in selected_id]
        ui.notify(f'Deleted row with ID {selected_id}')
        aggrid.update()
    
    async def delete_selected():
        selected = [row for row in await aggrid.get_selected_rows()][0]

        delete_course([selected['course_id'], selected['name']])

        ui.notify(f'Deleted course with ID {selected["course_id"]}')

        rows.clear()
        rows.extend(get_course())
        aggrid.update()

    with ui.row().classes('items-left'):
        ui.button('Delete selected', on_click=delete_selected)
        ui.button('New Row ', on_click=add_row)
        ui.label('Current Courses')

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_row_select_change)
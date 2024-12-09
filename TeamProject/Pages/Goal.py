from nicegui import ui
from TeamProject.Utilities import MySql, Validation

def get_goal():
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        code,
        name,
        level,
        course_id,
        description
    FROM goal    
    """
    cursor.execute(stmt)
    rows = cursor.fetchall()

    conn.close()
    return rows

def insert_goal(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO goal
    (
        code,
        name,
        level,
        course_id,
        description
    )
    VALUES (%s, %s, %s, %s, %s)    
    """
    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def update_goal(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    UPDATE goal
    SET description = %s
    WHERE code = %s
    """
    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def delete_goal(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    DELETE FROM goal
    WHERE code = %s AND name = %s AND level = %s
    """
    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def handle_save(ui, dialog, inputs):
    if Validation.check_entries(ui, inputs):
        dialog.submit([field.value for field in inputs.values()])

def page():

    rows = get_goal()
    
    columns = [
        {'field': 'code', 'editable': False, 'sortable': True},
        {'field': 'name', 'editable': False, 'sortable': True},
        {'field': 'level', 'editable': False, 'sortable': True},
        {'field': 'course_id', 'editable': False, 'sortable': True},
        {'field': 'description', 'editable': True},
    ]

    async def add_row():
        with ui.dialog() as dialog, ui.card():
            inputs = {
                'Goal Code': ui.input(label='Type Goal Code'),
                'Degree Name': ui.input(label='Type Degree Name'),
                'Degree Level': ui.input(label='Type Degree Level'),
                'Course Id': ui.input(label='Type Course Id'),
                'Goal Description': ui.input(label='Goal Description')
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
        
        insert_goal(result)

        ui.notify(f'Goal Added', color="positive")

        rows.clear()
        rows.extend(get_goal())
        aggrid.update()

    async def delete_selected():
        selected = [row for row in await aggrid.get_selected_rows()][0]

        delete_goal([selected["code"],selected["name"], selected["level"]])
        ui.notify(f'Deleted goal with Code {selected["code"]} Name: {selected["name"]} Level: {selected["level"] }', color="positive")

        rows.clear()
        rows.extend(get_goal())
        aggrid.update()

    
    async def update_description_change(e):
        row = e.args["data"]

        newVal = e.args['newValue']
        update_goal([newVal, row['code']])
        ui.notify(f'Updated goal description: {newVal}', color="positive")

        rows.clear()
        rows.extend(get_goal())
        aggrid.update()

    with ui.row().classes('items-left'):
        ui.button('Remove Goal', on_click=delete_selected)
        ui.button('New Goal', on_click=add_row)

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on("cellValueChanged", update_description_change)
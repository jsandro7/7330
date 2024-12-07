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
        description
    )
    VALUES (%s, %s, %s, %s)    
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
        {'field': 'description', 'editable': True},
    ]

    async def add_row():
        with ui.dialog() as dialog, ui.card():
            inputs = {
                'Goal Code': ui.input(label='Type Goal Code'),
                'Degree Name': ui.input(label='Type Degree Name'),
                'Degree Level': ui.input(label='Type Degree Level'),
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
        insert_goal(result)

        rows.clear()
        rows.extend(get_goal())
        aggrid.update()

    async def delete_selected():
        selected = [row for row in await aggrid.get_selected_rows()][0]

        delete_goal([selected["code"],selected["name"], selected["level"]])
        ui.notify(f'Deleted goal with Code {selected["code"]} Name: {selected["name"]} Level: {selected["level"] }')

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
    })
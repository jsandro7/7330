from nicegui import ui
from TeamProject.Utilities import MySql, Validation

def get_instructor():
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        ID,
        name
    FROM instructor    
    """
    cursor.execute(stmt)
    rows = cursor.fetchall()

    conn.close()
    return rows

def delete_instructor(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    DELETE FROM instructor
    WHERE ID = %s 
    """
    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def insert_instructor(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO instructor
    (        
        ID,
        name
    )
    VALUES (%s, %s)    
    """
    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def update_instructor(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    UPDATE instructor
    SET 
        name = %s
    WHERE ID = %s
    """
    cursor.execute(stmt, args)
    conn.commit()
    conn.close()


def handle_save(ui, dialog, inputs):
    if Validation.check_entries(ui, inputs):
        dialog.submit([field.value for field in inputs.values()])

def page():

    rows = get_instructor()

    columns = [
        {'field': 'ID', 'editable': False, },
        {'field': 'name', 'editable': True, 'sortable': True},
    ]
    
    async def add_row():
        with ui.dialog() as dialog, ui.card():
            inputs = {
                'Instructor ID': ui.input(label='Type ID'),
                'Instructor Name': ui.input(label='Type Name')
            }
            # Save and Cancel buttons
            with ui.row():
                ui.button(
                    'Save',
                    on_click=lambda: handle_save(ui, dialog, inputs)
                )
                ui.button('Cancel', on_click=lambda: dialog.close())


        result = await dialog
        insert_instructor(result)

        rows.clear()
        rows.extend(get_instructor())
        aggrid.update()

    
    async def update_name_change(e):
        row = e.args["data"]

        update_instructor([e.args['newValue'], row['ID']])
        ui.notify(f'Updated instructor Name: {e.args['newValue']}')

        rows.clear()
        rows.extend(get_instructor())
        aggrid.update()

       
    async def delete_row():
        selected = [row for row in await aggrid.get_selected_rows()][0]

        delete_instructor([selected['ID']])

        ui.notify(f'Deleted instructor ID: {selected["ID"]}, Name: {selected["name"]}')

        rows.clear()
        rows.extend(get_instructor())
        aggrid.update()

    with ui.row().classes('items-left'):
        ui.button('Remove Instructor', on_click=delete_row)
        ui.button('New Instructor', on_click=add_row)        

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on("cellValueChanged", update_name_change)
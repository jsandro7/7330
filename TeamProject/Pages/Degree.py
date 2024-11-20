from nicegui import ui
from TeamProject.Utilities import MySql

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

def page():

    rows = get_degrees()

    columns = [
        {'field': 'name', 'editable': False, 'sortable': True},
        {'field': 'level', 'editable': False, 'sortable': True},
    ]

    async def add_row(r):

        with ui.dialog() as dialog, ui.card():
            first = ui.input(label="Type Degree Name")
            second = ui.input(label="Type Degree level")
            with ui.row():
                ui.button('Save', on_click=lambda: dialog.submit([first.value, second.value]))
                ui.button('Cancel', on_click=lambda: dialog.close)


        result = await dialog
        insert_degree(result)

        rows.clear()
        rows.extend(get_degrees())
        aggrid.update()


    def handle_cell_value_change(e):
        new_row = e.args['data']
        ui.notify(f'Updated row to: {e.args["data"]}')
        rows[:] = [row | new_row if row['id'] == new_row['id'] else row for row in rows]

    async def delete_selected():
        selected_id = [row['id'] for row in await aggrid.get_selected_rows()]
        rows[:] = [row for row in rows if row['id'] not in selected_id]
        ui.notify(f'Deleted row with ID {selected_id}')
        aggrid.update()

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'single',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    ui.button('Delete selected', on_click=delete_selected)
    ui.button('New row', on_click=add_row)
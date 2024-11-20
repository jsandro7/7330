from nicegui import ui
from nicegui.events import ValueChangeEventArguments

def get_degrees(conn):
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        name,
        level
    FROM degree    
    """

    cursor.execute(stmt)
    rows = cursor.fetchall()

    return rows


def insert_degree(conn, args):
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



def page(conn):

    rows = get_degrees(conn)

    columns = [
        {'field': 'name', 'editable': True, 'sortable': True},
        {'field': 'level', 'editable': True},
    ]

    async def add_row():

        with ui.dialog() as dialog, ui.card():
            first = ui.input(label="Type Degree Name")
            second = ui.input(label="Type Degree level")
            with ui.row():
                ui.button('Save', on_click=lambda: dialog.submit([first.value, second.value]))
                ui.button('Cancel', on_click=lambda: dialog.close)


        result = await dialog
        insert_degree(conn, result)
        r = get_degrees(conn)
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
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    ui.button('Delete selected', on_click=delete_selected)
    ui.button('New row', on_click=add_row)
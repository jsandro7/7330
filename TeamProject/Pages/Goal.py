from nicegui import ui
from TeamProject.Utilities import MySql

def get_goal():
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        goal,
        name,
        level,
        description
    FROM goal    
    """

    cursor.execute(stmt)
    rows = cursor.fetchall()

    conn.close()

    return rows

def page():

    rows = get_goal()

    columns = [
        {'field': 'goal', 'editable': False, 'sortable': True},
        {'field': 'name', 'editable': False, 'sortable': True},
        {'field': 'level', 'editable': False, 'sortable': True},
        {'field': 'description', 'editable': True},
    ]

    def add_row():
        pass

    def handle_cell_value_change(e):
        pass

    async def delete_selected():
        pass

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    ui.button('Delete selected', on_click=delete_selected)
    ui.button('New row', on_click=add_row)
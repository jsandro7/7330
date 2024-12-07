from nicegui import ui
from TeamProject.Utilities import MySql

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

def page():

    rows = get_instructor()

    columns = [
        {'field': 'ID', 'editable': False, },
        {'field': 'name', 'editable': True, 'sortable': True},
    ]
    
    columnsCourse = [
        {'field': 'section_id', 'editable': False, 'sortable': True},
        {'field': 'courseId', 'editable': False, 'sortable': True},
        {'field': 'semester_code', 'editable': False, 'sortable': True},
    ]

    rowsCourse = []

    async def add_row():
        pass

    async def handle_cell_value_change(e):
        pass

    async def delete_selected():
        pass

    async def deleteTeaches_selected():
        pass

    async def add_Teaches():
        pass
    

    with ui.row().classes('items-left'):
        ui.button('Remove Instructor', on_click=delete_selected)
        ui.button('New Instructor', on_click=add_row)        

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    with ui.row().classes('items-left'):
        ui.button('Remove Section From Instructor', on_click=deleteTeaches_selected)
        ui.button('Assign Section To Instructor', on_click=add_Teaches)

    aggridCourse = ui.aggrid({
        'columnDefs': columnsCourse,
        'rowData': rowsCourse,
        'rowSelection': 'single',
        'stopEditingWhenCellsLoseFocus': True,
    })
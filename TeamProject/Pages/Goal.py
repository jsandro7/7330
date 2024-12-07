from nicegui import ui
from TeamProject.Utilities import MySql

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

def page():

    rows = get_goal()
    
    columns = [
        {'field': 'code', 'editable': False, 'sortable': True},
        {'field': 'name', 'editable': False, 'sortable': True},
        {'field': 'level', 'editable': False, 'sortable': True},
        {'field': 'description', 'editable': True},
    ]

    rowsEval = []

    columnsEval = [
        {'field': 'course_id', 'editable': False, 'sortable': True},
        {'field': 'name', 'editable': False, 'sortable': True},
    ]
      

    def add_row():
        pass

    def handle_cell_value_change(e):
        pass

    async def delete_selected():
        pass

    async def delete_eval():
        pass

    async def add_eval():
        pass


    with ui.row().classes('items-left'):
        ui.button('Remove Goal', on_click=delete_selected)
        ui.button('New Goal', on_click=add_row)


    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    with ui.row().classes('items-left'):
        ui.button('Remove Evaluation From Goal', on_click=delete_eval)
        ui.button('Enter Evaluation To Goal', on_click=add_eval)

    aggridCourse = ui.aggrid({
        'columnDefs': columnsEval,
        'rowData': rowsEval,
        'rowSelection': 'single',
        'stopEditingWhenCellsLoseFocus': True,
    })
from nicegui import ui
from TeamProject.Utilities import MySql, Validation

def get_data():
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        section_id,
        code,
        evaluation_method,
        comment,
        A_count,
        B_count,
        C_count,
        F_count
    FROM evaluation    
    """
    cursor.execute(stmt)
    rows = cursor.fetchall()

    conn.close()
    return rows

def page():

    rows = get_data()
    
    columns = [
        {'name': 'section_id', 'field': 'section_id', 'label': 'Section', 'editable': False},
        {'name': 'code', 'field': 'code', 'label': 'Goal Code', 'editable': False},
        {'name': 'evaluation_method', 'field': 'evaluation_method', 'label': 'Method', 'editable': False},
        {'name': 'A_count', 'field': 'A_count', 'label': 'A Count', 'editable': False},
        {'name': 'B_count', 'field': 'B_count', 'label': 'B count', 'editable': False},
        {'name': 'C_count', 'field': 'C_count', 'label': 'C count', 'editable': False},
        {'name': 'F_count', 'field': 'F_count', 'label': 'F count', 'editable': False},
        {'name': 'comment', 'field':'comment', 'label': 'Comments', 'editable': False}       
    ]

    def add_row():
        pass

    def handle_cell_value_change(e):
        pass

    async def delete_selected():
        pass

    with ui.row().classes('items-left'):
        ui.button('Remove Evaluation', on_click=delete_selected)
        ui.button('New Evaluation', on_click=add_row)


    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)
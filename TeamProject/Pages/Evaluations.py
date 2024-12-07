from nicegui import ui
from TeamProject.Utilities import MySql

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
        {'name': 'section_id', 'field': 'section_id', 'label': 'Section'},
        {'name': 'code', 'field': 'code', 'label': 'Goal Code'},
        {'name': 'evaluation_method', 'field': 'evaluation_method', 'label': 'Method'},
        {'name': 'A_count', 'field': 'A_count', 'label': 'A Count'},
        {'name': 'B_count', 'field': 'B_count', 'label': 'B count'},
        {'name': 'C_count', 'field': 'C_count', 'label': 'C count'},
        {'name': 'F_count', 'field': 'F_count', 'label': 'F count'},
        {'name': 'comment', 'field':'comment', 'label': 'Comments'}       
    ]

    async def update():
        pass
    

    with ui.row().classes('items-left'):
        ui.button('TODO', on_click=update)
             

    ui.table(
        rows=rows, columns=columns, 
        column_defaults={
        'align': 'left',
        'headerClasses': 'uppercase text-primary'},
    )
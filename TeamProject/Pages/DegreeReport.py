from nicegui import ui
from TeamProject.Utilities import MySql

def get_data():
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

def page():

    rows = get_data()

    columns = [
         {'name': 'name', 'field': 'name', 'label': 'Name'},
        {'name': 'level', 'field':'level', 'label': 'Level' }       
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

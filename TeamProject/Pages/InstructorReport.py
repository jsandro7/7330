from nicegui import ui
from TeamProject.Utilities import MySql

def get_data():
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

    rows = get_data()

    columns = [        
        {'name': 'ID', 'field':'ID', 'label': 'ID'},    
        {'name': 'name', 'field': 'name', 'label': 'Name'}   
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
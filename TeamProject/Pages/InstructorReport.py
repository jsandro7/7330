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

    async def filter_sections():
        pass
    


    # Input fields
    with ui.row().classes("items-left"):        
        start_year_input = ui.input("Start Year", placeholder="Enter Start Year").classes("w-48")
        start_semester_input = ui.select(["SP", "SM", "FA"], label="Start Semester").classes("w-48")
        end_year_input = ui.input("End Year", placeholder="Enter End Year").classes("w-48")
        end_semester_input = ui.select(["SP", "SM", "FA"], label="End Semester").classes("w-48")

        ui.button("Filter Sections", on_click=filter_sections)

    table = ui.table(
        rows=rows,
        columns=columns,
        column_defaults={"align": "left", "headerClasses": "uppercase text-primary"},
    )
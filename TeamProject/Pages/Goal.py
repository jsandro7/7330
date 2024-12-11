from nicegui import ui
from TeamProject.Utilities import MySql, Validation

def get_goal():
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        code,
        name,
        level,
        course_id,
        description
    FROM goal    
    """
    cursor.execute(stmt)
    rows = cursor.fetchall()

    conn.close()
    return rows

def get_degrees():
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT        
        name       
    FROM degree    
    """
    cursor.execute(stmt)
    rows = cursor.fetchall()

    conn.close()
    return rows


def insert_goal(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO goal
    (
        code,
        name,
        level,
        course_id,
        description
    )
    VALUES (%s, %s, %s, %s, %s)    
    """
    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def update_goal(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    UPDATE goal
    SET description = %s
    WHERE code = %s
    """
    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def delete_goal(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    DELETE FROM goal
    WHERE code = %s AND name = %s AND level = %s
    """
    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def get_courses():
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        course_id,
        name
    FROM course    
    """
    cursor.execute(stmt)
    rows = cursor.fetchall()
    conn.close()

    return rows

def handle_save(ui, dialog, inputs):
    if Validation.check_entries(ui, inputs):
        dialog.submit([field.value for field in inputs.values()])

def page():

    rows = get_goal()
    
    columns = [
        {'field': 'code', 'editable': False, 'sortable': True},
        {'field': 'name', 'editable': False, 'sortable': True},
        {'field': 'level', 'editable': False, 'sortable': True},
        {'field': 'course_id', 'editable': False, 'sortable': True},
        {'field': 'description', 'editable': True},
    ]

    async def add_row():

        degrees = get_degrees()
        degree_options = {
            degree["name"]: f"{degree['name']}"
            for degree in degrees
        }    

        courses = get_courses()
        course_options = {
            course["course_id"]: f"{course['name']}"
            for course in courses
        }      

        with ui.dialog() as dialog, ui.card():
            inputs = {
                'Goal Code': ui.input(label='Type Goal Code'),
                'Degree Name': ui.select(degree_options, label="Select Degree").classes("w-48"),
                'Degree Level': ui.select(["BA", "BS", "MS", 'Ph.D'], label="Select Level").classes("w-48"),
                'Course Id': ui.select(course_options, label="Select Course").classes("w-48"),
                'Goal Description': ui.input(label='Goal Description')
            }
            # Save and Cancel buttons
            with ui.row():
                ui.button(
                    'Save',
                    on_click=lambda: handle_save(ui, dialog, inputs)
                )
                ui.button('Cancel', on_click=lambda: dialog.close())

        result = await dialog
        
        if(result is None):
            return
        
        insert_goal(result)

        ui.notify(f'Goal Added', color="positive")

        rows.clear()
        rows.extend(get_goal())
        aggrid.update()

    async def delete_selected():
        selected = [row for row in await aggrid.get_selected_rows()][0]

        delete_goal([selected["code"],selected["name"], selected["level"]])
        ui.notify(f'Deleted goal with Code {selected["code"]} Name: {selected["name"]} Level: {selected["level"] }', color="positive")

        rows.clear()
        rows.extend(get_goal())
        aggrid.update()

    
    async def update_description_change(e):
        row = e.args["data"]

        newVal = e.args['newValue']
        update_goal([newVal, row['code']])
        ui.notify(f'Updated goal description: {newVal}', color="positive")

        rows.clear()
        rows.extend(get_goal())
        aggrid.update()

    with ui.row().classes('items-left'):
        ui.button('Remove Goal', on_click=delete_selected)
        ui.button('New Goal', on_click=add_row)

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on("cellValueChanged", update_description_change)
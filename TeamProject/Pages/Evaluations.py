from nicegui import ui

from TeamProject.Pages.Instructor import get_instructor
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

def get_methods():
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        name
    FROM eval_methods
    """
    cursor.execute(stmt)
    rows = cursor.fetchall()

    conn.close()
    return rows

def insert_method(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO eval_methods
    (
        name
    )
    VALUES (%s)    
    """
    cursor.execute(stmt, args)
    conn.commit()
    conn.close()


def get_goals(args):
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT       
        code,
        description
    FROM goal g
    JOIN section s ON g.course_id = s.course_id
    where s.section_id = %s 
    """
    cursor.execute(stmt, args)
    rows = cursor.fetchall()

    conn.close()
    return rows

def delete_eval(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    DELETE FROM evaluation
    WHERE code = %s AND section_id = %s
    """
    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def get_filtered_sections(args):
    """
    Retrieves sections taught by a specific instructor during a given semester and year.
    """
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT 
        s.section_id,
        s.course_id,
        c.name AS course_name,
        s.student_enrolled
    FROM 
        section s
    JOIN 
        course c ON s.course_id = c.course_id
    WHERE 
        s.ID = %s AND s.year = %s AND s.semester = %s 
    ORDER BY 
        s.section_id
    """
    cursor.execute(stmt, args)
    rows = cursor.fetchall()

    conn.close()
    return rows

def update_evaluation(section_id, code, field, new_value):
    """
    Update the evaluation record in the database.
    """
    conn = MySql.create_conn()
    cursor = conn.cursor()

    # Construct the update query dynamically based on the edited field
    stmt = f"""
    UPDATE evaluation
    SET {field} = %s
    WHERE section_id = %s AND code = %s
    """
    try:
        cursor.execute(stmt, (new_value, section_id, code))
        conn.commit()
        ui.notify(f'Updated {field} to {new_value} for section_id {section_id}', color="positive")
    except Exception as e:
        ui.notify(f'Failed to update evaluation: {e}', color="negative")
    finally:
        conn.close()

def get_section_info(section_id):
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)
    stmt = """
    SELECT 
        e.section_id,
        e.code,
        e.evaluation_method,
        e.comment,
        e.A_count,
        e.B_count,
        e.C_count, 
        e.F_count
    FROM 
        evaluation e
    WHERE 
        e.section_id = %s 
    ORDER BY 
        e.section_id
    """
    # Wrap section_id in a tuple
    cursor.execute(stmt, (section_id,))
    rows = cursor.fetchall()
    return rows

def insert_evalution(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO evaluation
    (
        section_id,
        name,
        level,
        code,
        evaluation_method,
        comment,
        A_count,
        B_count,
        C_count, 
        F_count         
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)    
    """
    cursor.execute(stmt, args)
    conn.commit()
    conn.close()


def get_related_degree(args):
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT       
        dc.name,
        dc.level
    FROM course c
    JOIN section s ON c.course_id = s.course_id
    JOIN degree_course dc ON c.course_id = dc.course_id
    WHERE s.section_id = %s 
    LIMIT 1
    """
    cursor.execute(stmt, args)
    rows = cursor.fetchall()

    conn.close()
    return rows

def handle_save(ui, dialog, inputs):
    if Validation.check_entries(ui, inputs):
        dialog.submit([field.value for field in inputs.values()])

def page():
    rows = []

    instructors = get_instructor()
    instructors_options = {
        instructor["ID"]: f"{instructor['name']}"
        for instructor in instructors
    }

    columns = [
        {'name': 'section_id', 'field': 'section_id', 'label': 'Section', 'editable': False},
        {'name': 'course_id', 'field': 'course_id', 'label': 'Course ID', 'editable': False},
        {'name': 'course_name', 'field': 'course_name', 'label': 'Course Name', 'editable': False},
        {'name': 'student_enrolled', 'field': 'student_enrolled', 'label': 'Students Enrolled', 'editable': False},
    ]

    eval_columns = [
        {'name': 'section_id', 'field': 'section_id', 'label': 'Section Id', 'editable': False},
        {'name': 'code', 'field': 'code', 'label': 'Code', 'editable': False},
        {'name': 'evaluation_method', 'field': 'evaluation_method', 'label': 'Course Name', 'editable': True},
        {'name': 'A_count', 'field': 'A_count', 'label': 'A_count', 'editable': True},
        {'name': 'B_count', 'field': 'B_count', 'label': 'B_count', 'editable': True},
        {'name': 'C_count', 'field': 'C_count', 'label': 'C_count', 'editable': True},
        {'name': 'F_count', 'field': 'F_count', 'label': 'F_count', 'editable': True},
        {'name': 'comment', 'field': 'comment', 'label': 'comment', 'editable': True},

    ]

    filtered_rows = []
    eval_rows = []
    async def filter_sections():
        """
        Filters sections based on the selected instructor, semester, and year.
        """
        if not instructor_input.value or not semester_input.value:
            ui.notify("All fields are required!", color="negative")
            return

        nonlocal filtered_rows
        filtered_rows = get_filtered_sections([
            instructor_input.value,
            start_year_input.value,
            semester_input.value]
        )

        # Update the table with filtered rows
        aggrid.options['rowData'] = filtered_rows
        aggrid.update()

    def on_cell_value_changed(event):
        """
        Handle cell value changes and update the server.
        """
        # Extract relevant information from the event
        updated_data = event.args.get('data')  # Full row data
        updated_value = event.args.get('value')  # New value for the cell
        field = event.args.get('colId')  # Column ID of the edited cell

        if updated_data and updated_value is not None:
            section_id = updated_data['section_id']
            code = updated_data['code']

            update_evaluation(section_id, code, field, updated_value)


    def on_cell_click(event):
        """
        Event handler for cell clicks. Prints the section_id of the clicked cell.
        """
        if event.args and "data" in event.args and "section_id" in event.args["data"]:
            section_id = event.args["data"]["section_id"]

            eval_rows = get_section_info(section_id)
            eval_aggrid.options['rowData'] = eval_rows
            eval_aggrid.update()

    async def deleteEval_selected():
        selected = [row for row in await eval_aggrid.get_selected_rows()][0]

        delete_eval([selected['code'], selected['section_id']])

        ui.notify(f'Deleted eval', color="positive")

        eval_rows = get_section_info(selected['section_id'])
        eval_aggrid.options['rowData'] = eval_rows
        eval_aggrid.update()

    async def add_Eval():

        selectedSection = [row for row in await aggrid.get_selected_rows()][0]

        goals = get_goals([selectedSection['section_id']])
        goals_options = {
            goal["code"]: f"{goal['description']}"
            for goal in goals
        }

        methods = get_methods()
        methods_options = {
            method["name"]: f"{method['name']}"
            for method in methods
        }

        with ui.dialog() as dialog, ui.card():
            inputs = {
                'Code' : ui.select(goals_options, label="Select Goal").classes("w-48"),
                'Evaluation_method' : ui.select(methods_options, label="Select Method").classes("w-48"),
                'Comment': ui.input(label='Type Comment'),
                'Number_A_students': ui.input(label='A Students'),
                'Number_B_students': ui.input(label='B Students'),
                'Number_C_students': ui.input(label='C Students'),
                'Number_F_students': ui.input(label='F Students'),
            }
            # Save and Cancel buttons
            with ui.row():
                ui.button(
                    'Save',
                    on_click=lambda: handle_save(ui, dialog, inputs)
                )
                ui.button('Cancel', on_click=lambda: dialog.close())

        result = await dialog       

        if(not result):
            return   


        degree = get_related_degree([selectedSection['section_id']])[0]    

        
        newList = [selectedSection['section_id'], degree['name'], degree['level'], result[0], result[1],result[2], int(result[3]), int(result[4]),int(result[5]),int(result[6])]

        insert_evalution(newList)

        ui.notify(f'Evaluation added', color="positive")

        eval_rows = get_section_info(selectedSection['section_id'])
        eval_aggrid.options['rowData'] = eval_rows
        eval_aggrid.update()


    async def add_method():
        with ui.dialog() as dialog, ui.card():
            inputs = {
                'Name': ui.input(label='Type in new method name')
            }
            # Save and Cancel buttons
            with ui.row():
                ui.button(
                    'Save',
                    on_click=lambda: handle_save(ui, dialog, inputs)
                )
                ui.button('Cancel', on_click=lambda: dialog.close())

        result = await dialog

        if(not result):
            return       

        insert_method(result)

        ui.notify(f'Evaluation Method Added', color="positive")


    with ui.row().classes("items-left"):
        instructor_input = ui.select(instructors_options, label="Instructor").classes("w-48")
        start_year_input = ui.input("Year", placeholder="Enter Year").classes("w-48")
        semester_input = ui.select(["SP", "SM", "FA"], label="Semester").classes("w-48")     

        ui.button("Filter Sections", on_click=filter_sections)

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('rowSelected', on_cell_click)

    with ui.row().classes('items-left'):
        ui.button('Remove Evaluation', on_click=deleteEval_selected)
        ui.button('Add Evaluation', on_click=add_Eval)
        ui.button('New Evaluation Method', color='red', on_click=add_method)

    eval_aggrid = ui.aggrid({
        'columnDefs': eval_columns,
        'rowData': eval_rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', on_cell_value_changed)














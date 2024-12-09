from nicegui import ui
from TeamProject.Utilities import MySql, Validation

def get_course():
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

def get_course_sections(args):
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        s.section_id,
        s.course_id,
        s.ID,
        s.semester,
        s.year,
        s.student_enrolled
    FROM section s
    JOIN course c ON c.course_id = s.course_id
    WHERE c.course_id = %s
    """

    cursor.execute(stmt, args)
    rows = cursor.fetchall()

    conn.close()

    return rows

def insert_course(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO course
    (
        course_id,
        name
    )
    VALUES (%s, %s)    
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def delete_course(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    DELETE FROM course
    WHERE course_id = %s
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def insert_section(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO section
    (
        section_id,
        course_id,
        ID,
        semester,
        year,
        student_enrolled
    )
    VALUES (%s, %s, %s, %s, %s, %s)    
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def delete_section(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    DELETE FROM section
    WHERE ID = %s
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def handle_save(ui, dialog, inputs):
    if Validation.check_entries(ui, inputs):
        dialog.submit([field.value for field in inputs.values()])

def page():

    rows = get_course()

    columns = [
        {'field': 'course_id', 'editable': False, },
        {'field': 'name', 'editable': True, 'sortable': True},
    ]

    columnsSection = [
        {'field': 'section_id', 'editable': False, 'sortable': True},
        {'field': 'course_id', 'editable': False, 'sortable': True},
        {'field': 'id', 'editable': False, 'sortable': True},
        {'field': 'semester', 'editable': False, 'sortable': True},
        {'field': 'year', 'editable': False, 'sortable': True},
        {'field': 'students_enrolled', 'editable': False, 'sortable': True},
    ]

    rowsSection = []

    async def add_row():
        with ui.dialog() as dialog, ui.card():
            inputs = {
                'Course ID': ui.input(label='Type Course ID'),
                'Course Name': ui.input(label='Type Course Name')
            }
            # Save and Cancel buttons
            with ui.row():
                ui.button(
                    'Save',
                    on_click=lambda: handle_save(ui, dialog, inputs)
                )
                ui.button('Cancel', on_click=lambda: dialog.close())


        result = await dialog
        insert_course(result)

        rows.clear()
        rows.extend(get_course())
        aggrid.update()
    
    async def add_section():
        with ui.dialog() as dialog, ui.card():
            inputs = {
                'Section ID': ui.input(label='Type Section ID'),
                'ID': ui.input(label='Type Instructor ID'),
                'Semester': ui.input(label='Type Semester'),
                'Year': ui.input(label='Type Year'),
                'Students Enrolled': ui.input(label='Type Students Enrolled')
            }
            # Save and Cancel buttons
            with ui.row():
                ui.button(
                    'Save',
                    on_click=lambda: handle_save(ui, dialog, inputs)
                )
                ui.button('Cancel', on_click=lambda: dialog.close())

        result = await dialog

        selectedCourse = [row for row in await aggrid.get_selected_rows()][0]

        result.extend([selectedCourse['course_id']])

        insert_section(result)

        rowsSection.clear()
        rowsSection.extend(get_course_sections([selectedCourse['course_id']]))
        aggridSection.update()

    async def handle_row_select_change(e):
        selected = [row for row in await aggrid.get_selected_rows()][0]

        result = get_course_sections([selected['course_id']])

        rows.clear()
        rows.extend(result)
        rows.update()
    
    async def delete_selected():
        selected = [row for row in await aggrid.get_selected_rows()][0]

        delete_course([selected['course_id']])

        ui.notify(f'Deleted course with ID {selected["course_id"]}')

        rows.clear()
        rows.extend(get_course())
        aggrid.update()
    
    async def deleteSection_selected():
        selected = [row for row in await aggridSection.get_selected_rows()][0]
        selectedCourse = [row for row in await aggrid.get_selected_rows()][0]

        delete_section([selected['section_id']])    

        ui.notify(f'Deleted section with ID {selected["section_id"]}')    

        rowsSection.clear()
        rowsSection.extend(get_course_sections([selectedCourse['course_id']]))
        aggridSection.update()

    with ui.row().classes('items-left'):
        ui.button('Remove Course', on_click=delete_selected)
        ui.button('New Course', on_click=add_row)

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_row_select_change)

    with ui.row().classes('items-left'):
        ui.button('Remove Section From Course', on_click=delete_section)
        ui.button('Assign Section To Course', on_click=add_section)

    aggridSection = ui.aggrid({
        'columnDefs': columnsSection,
        'rowData': rowsSection,
        'rowSelection': 'single',
        'stopEditingWhenCellsLoseFocus': True,
    })

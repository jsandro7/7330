from nicegui import ui
from TeamProject.Utilities import MySql

def get_degrees():
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

def get_degrees_courses(args):
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT 
        c.course_id,
        c.name,
        dc.is_core
    FROM degree d
    JOIN degree_course dc ON d.name = dc.name AND d.level = dc.level
    JOIN course c ON c.course_id = dc.course_id  
    WHERE d.name = %s AND d.level = %s
    """

    cursor.execute(stmt, args)
    rows = cursor.fetchall()

    conn.close()

    return rows

def get_degrees_sections(args):
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT   
        dc.name AS "Degree_Name",
        dc.level AS "Degree_Level",     
        s.section_id AS "Section_ID",
        s.course_id AS "Course_Id",
        c.name AS "Course_Name",
        CASE s.semester
                WHEN 'SP' THEN 'Spring'
                WHEN 'SM' THEN 'Summer'
                WHEN 'FA' THEN 'Fall'
		END AS semester,
        s.year
    FROM section s    
    JOIN course c ON c.course_id = s.course_id
    JOIN degree_course dc ON dc.course_id = c.course_id
    WHERE 
        dc.name = %s AND 
        dc.level = %s AND
        (s.year * 10 + 
            CASE s.semester
                WHEN 'SP' THEN 1
                WHEN 'SM' THEN 2
                WHEN 'FA' THEN 3
            END
        ) BETWEEN 
        (%s * 10 + 
            CASE %s
                WHEN 'SP' THEN 1
                WHEN 'SM' THEN 2
                WHEN 'FA' THEN 3
            END
        ) AND 
        (%s * 10 + 
            CASE %s
                WHEN 'SP' THEN 1
                WHEN 'SM' THEN 2
                WHEN 'FA' THEN 3
            END
        )
    """

    cursor.execute(stmt, args)
    rows = cursor.fetchall()

    conn.close()
    return rows

def page():

    rowsCourses = []

    columnsCourses = [
        {'name': 'course_id', 'field':'course_id', 'label': 'Course ID' },
        {'name': 'name', 'field': 'name', 'label': 'Course Name'},
        {'name': 'is_core', 'field':'is_core', 'label': 'Is Core Course?' }       
    ]

    degrees = get_degrees()
    degrees_options = {
        f"{degree['name']}-{degree['level']}" : f"{degree['name']} - {degree['level']}"
        for degree in degrees
    }

    async def filter_degree_courses():
        if not (degrees_input.value):
            ui.notify("All fields are required!", color="negative")
            return

        try:
            nonlocal rowsCourses
            rowsCourses = get_degrees_courses(degrees_input.value.split('-'))
            
            table_courses.rows = rowsCourses
            ui.notify("Filter applied successfully!", color="positive")
        except Exception as e:
            ui.notify(f"Error: {e}", color="negative")
    
    ui.label('Degree Course:').style('font-size:25px; font-weight:bold; color:navy;')   

    with ui.row().classes("items-left"):     
        degrees_input = ui.select(degrees_options, label="Degrees").classes("w-48")           
        ui.button("Filter Sections", on_click=filter_degree_courses)
    
    

    table_courses =ui.table(
        rows=rowsCourses, columns=columnsCourses, 
        column_defaults={
        'align': 'left',
        'headerClasses': 'uppercase text-primary'},
    )

    ui.separator()

    rowsSections = []

    columnsSections = [
        {'name': 'Degree_Name', 'field':'Degree_Name', 'label': 'Degree Name' },
        {'name': 'Degree_Level', 'field':'Degree_Level', 'label': 'Degree Level' },
        {'name': 'Section_ID', 'field':'Section_ID', 'label': 'Section ID' },
        {'name': 'semester', 'field':'semester', 'label': 'Semester'},
        {'name': 'year', 'field':'year', 'label': 'Year'},
        {'name': 'Course_Id', 'field':'Course_Id', 'label': 'Course ID' },
        {'name': 'Course_Name', 'field': 'Course_Name', 'label': 'Course Name'}
    ]

    async def filter_degree_sections():
        if not (
                degrees_input.value and
                start_year_input.value and 
                start_semester_input.value and 
                end_year_input.value and 
                end_semester_input.value
                ):
            ui.notify("All fields are required!", color="negative")
            return

        try:
            nonlocal rowsSections

            listParam = degrees_input.value.split('-')

            listParam.extend([int(start_year_input.value),
                            start_semester_input.value,
                            int(end_year_input.value),
                            end_semester_input.value])

            rowsSections = get_degrees_sections(listParam)
            
            table_sections.rows = rowsSections
            ui.notify("Filter applied successfully!", color="positive")
        except Exception as e:
            ui.notify(f"Error: {e}", color="negative")
             

    ui.label('Degree Sections:').style('font-size:25px; font-weight:bold; color:navy;')

    with ui.row().classes("items-left"):     
        degrees_input = ui.select(degrees_options, label="Degrees").classes("w-48") 
        start_year_input = ui.input("Start Year", placeholder="Enter Start Year").classes("w-48")
        start_semester_input = ui.select(["SP", "SM", "FA"], label="Start Semester").classes("w-48")
        end_year_input = ui.input("End Year", placeholder="Enter End Year").classes("w-48")
        end_semester_input = ui.select(["SP", "SM", "FA"], label="End Semester").classes("w-48")          
        ui.button("Filter Sections", on_click=filter_degree_sections)
        
    table_sections =ui.table(
        rows=rowsSections, columns=columnsSections, 
        column_defaults={
        'align': 'left',
        'headerClasses': 'uppercase text-primary'},
    )

 

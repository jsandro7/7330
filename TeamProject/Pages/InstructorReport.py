from nicegui import ui
from TeamProject.Utilities import MySql

def get_instructors():
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

def get_data(args):
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT 
        i.ID AS "Instructor_ID",
        i.name AS "Instructor_Name",
        s.section_id AS "Section_ID",
        s.course_id AS "Course_Id",
        c.name AS "Course_Name",
        CASE s.semester
                WHEN 'SP' THEN 'Spring'
                WHEN 'SM' THEN 'Summer'
                WHEN 'FA' THEN 'Fall'
		END AS semester,
        s.year,
        s.student_enrolled
    FROM section s
    JOIN instructor i ON s.ID = i.ID
    JOIN course c ON c.course_id = s.course_id
    WHERE 
        s.ID = %s AND 
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

    rows = []

    columns = [        
        {'name': 'Instructor_ID', 'field':'Instructor_ID', 'label': 'Instructor ID'},  
        {'name': 'Instructor_Name', 'field':'Instructor_Name', 'label': 'Instructor Name'},
        {'name': 'Section_ID', 'field':'Section_ID', 'label': 'Section ID'},
        {'name': 'Course_Id', 'field':'Course_Id', 'label': 'Course Id'},
        {'name': 'Course_Name', 'field':'Course_Name', 'label': 'Course Name'},
        {'name': 'year', 'field':'year', 'label': 'Year'},
        {'name': 'semester', 'field':'semester', 'label': 'Semester'},
        {'name': 'student_enrolled', 'field': 'student_enrolled', 'label': 'Enrolled Students'}   
    ]

    instructors = get_instructors()
    instructors_options = {
        instructor["ID"]: f"{instructor['ID']}: {instructor['name']}"
        for instructor in instructors
    }

    async def filter_sections():
        if not (
            instructors_input.value and
            start_year_input.value and 
            start_semester_input.value and 
            end_year_input.value and 
            end_semester_input.value
        ):
            ui.notify("All fields are required!", color="negative")
            return

        try:
            nonlocal rows
            rows = get_data(                            
                            [instructors_input.value, 
                            int(start_year_input.value),
                            start_semester_input.value,
                            int(end_year_input.value),
                            end_semester_input.value
                            ]
            )

            table.rows = rows
            ui.notify("Filter applied successfully!", color="positive")
        except Exception as e:
            ui.notify(f"Error: {e}", color="negative")
    


    # Input fields
    with ui.row().classes("items-left"):     
        instructors_input = ui.select(instructors_options, label="Instructor").classes("w-48")   
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
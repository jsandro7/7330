from nicegui import ui
from TeamProject.Utilities import MySql, Validation


def get_courses():
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    # Query to fetch all courses for dropdown
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


def get_filtered_sections(
    course_id, start_year, start_semester, end_year, end_semester
):
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT 
        s.section_id,
        s.semester,
        s.year,
        c.course_id,
        c.name
    FROM section s
    JOIN course c ON c.course_id = s.course_id
    WHERE 
        c.course_id = %s AND 
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

    cursor.execute(
        stmt, (course_id, start_year, start_semester, end_year, end_semester)
    )
    rows = cursor.fetchall()
    conn.close()

    return rows


def page():
    rows = []

    # Fetch courses for dropdown in format of COURSEID: NAME
    courses = get_courses()
    course_options = {
        course["course_id"]: f"{course['course_id']}: {course['name']}"
        for course in courses
    }

    columns = [
        {"name": "section_id", "field": "section_id", "label": "Section ID"},
        {"name": "semester", "field": "semester", "label": "Semester"},
        {"name": "year", "field": "year", "label": "Year"},
        {"name": "course_id", "field": "course_id", "label": "Course ID"},
        {"name": "name", "field": "name", "label": "Course Name"},
    ]

    async def filter_sections():
        if not (
            start_year_input.value
            and start_semester_input.value
            and end_year_input.value
            and end_semester_input.value
            and course_input.value
        ):
            ui.notify("All fields are required!", color="negative")
            return

        try:
            nonlocal rows
            rows = get_filtered_sections(
                course_input.value,
                int(start_year_input.value),
                start_semester_input.value,
                int(end_year_input.value),
                end_semester_input.value,
            )
            table.rows = rows
            ui.notify("Filter applied successfully!", color="positive")
        except Exception as e:
            ui.notify(f"Error: {e}", color="negative")

    # Input fields
    with ui.row().classes("items-left"):
        course_input = ui.select(course_options, label="Course").classes("w-48")
        start_year_input = ui.input(
            "Start Year", placeholder="Enter Start Year"
        ).classes("w-48")
        start_semester_input = ui.select(
            ["SP", "SM", "FA"], label="Start Semester"
        ).classes("w-48")
        end_year_input = ui.input("End Year", placeholder="Enter End Year").classes(
            "w-48"
        )
        end_semester_input = ui.select(
            ["SP", "SM", "FA"], label="End Semester"
        ).classes("w-48")

        ui.button("Filter Sections", on_click=filter_sections)

    table = ui.table(
        rows=rows,
        columns=columns,
        column_defaults={"align": "left", "headerClasses": "uppercase text-primary"},
    )

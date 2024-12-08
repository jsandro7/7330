from nicegui import ui
from TeamProject.Utilities import MySql


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

# Gets the sections of a course in a semester where at least *min_percentage* students passed
def get_filtered_sections(course_id, semester_year, semester_term, min_percentage):
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        e.section_id,
        c.name AS course_name,
        s.semester AS semester_term,
        s.year AS semester_year,
        e.A_count + e.B_count + e.C_count AS passed_count,
        e.A_count + e.B_count + e.C_count + e.F_count AS total_count,
        ROUND(((e.A_count + e.B_count + e.C_count) / (e.A_count + e.B_count + e.C_count + e.F_count)) * 100, 2) AS pass_percentage
    FROM evaluation e
    JOIN section s ON e.section_id = s.section_id
    JOIN course c ON s.course_id = c.course_id
    WHERE s.course_id = %s
      AND s.year = %s
      AND s.semester = %s
      AND ROUND(((e.A_count + e.B_count + e.C_count) / (e.A_count + e.B_count + e.C_count + e.F_count)) * 100, 2) >= %s
    """
    cursor.execute(stmt, (course_id, semester_year, semester_term, min_percentage))
    rows = cursor.fetchall()

    conn.close()
    return rows


def page():
    rows = []

    courses = get_courses()
    course_options = {
        course["course_id"]: f"{course['course_id']}: {course['name']}"
        for course in courses
    }

    columns = [
        {"name": "section_id", "field": "section_id", "label": "Section ID"},
        {"name": "course_name", "field": "course_name", "label": "Course Name"},
        {"name": "semester_term", "field": "semester_term", "label": "Semester"},
        {"name": "semester_year", "field": "semester_year", "label": "Year"},
        {
            "name": "pass_percentage",
            "field": "pass_percentage",
            "label": "Pass Percentage",
        },
    ]

    async def filter_sections():
        if not (
            course_input.value
            and semester_year_input.value
            and semester_term_input.value
            and percentage_input.value
        ):
            ui.notify("All fields are required!", color="negative")
            return

        try:
            nonlocal rows

            semester_year = int(semester_year_input.value)
            semester_term = semester_term_input.value
            min_percentage = float(percentage_input.value)

            rows = get_filtered_sections(
                course_input.value,
                semester_year,
                semester_term,
                min_percentage,
            )
            table.rows = rows
            ui.notify("Filter applied successfully!", color="positive")
        except Exception as e:
            ui.notify(f"Error: {e}", color="negative")

    # Input Fields
    with ui.row().classes("items-left"):
        course_input = ui.select(course_options, label="Course").classes("w-48")
        semester_year_input = ui.input(
            "Semester Year", placeholder="Enter Year (e.g., 2024)"
        ).classes("w-48")
        semester_term_input = ui.select(["SP", "SM", "FA"], label="Semester").classes(
            "w-48"
        )
        percentage_input = ui.input(
            "Minimum Percentage", placeholder="Enter % (e.g., 75)"
        ).classes("w-48")

        ui.button("Filter Sections", on_click=filter_sections)

    table = ui.table(
        rows=rows,
        columns=columns,
        column_defaults={"align": "left", "headerClasses": "uppercase text-primary"},
    )

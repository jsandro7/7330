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
        ROUND(((e.A_count + e.B_count + e.C_count) / 
               (e.A_count + e.B_count + e.C_count + e.F_count)) * 100, 2) AS pass_percentage
    FROM evaluation e
    JOIN section s ON e.section_id = s.section_id
    JOIN course c ON s.course_id = c.course_id
    WHERE s.course_id = %s
      AND s.year = %s
      AND s.semester = %s
      AND ROUND(((e.A_count + e.B_count + e.C_count) / 
                 (e.A_count + e.B_count + e.C_count + e.F_count)) * 100, 2) >= %s
    """
    cursor.execute(stmt, (course_id, semester_year, semester_term, min_percentage))
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_all_sections_with_evaluation_status(semester_year, semester_term):
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        s.section_id,
        c.name AS course_name,
        s.semester AS semester_term,
        s.year AS semester_year,
        CASE
            WHEN e.evaluation_method IS NOT NULL 
                 AND e.A_count IS NOT NULL 
                 AND e.B_count IS NOT NULL 
                 AND e.C_count IS NOT NULL 
                 AND e.F_count IS NOT NULL THEN 'Complete'
            WHEN e.evaluation_method IS NOT NULL 
                 OR e.A_count IS NOT NULL 
                 OR e.B_count IS NOT NULL 
                 OR e.C_count IS NOT NULL 
                 OR e.F_count IS NOT NULL THEN 'Partially Entered'
            ELSE 'Not Entered'
        END AS evaluation_status
    FROM section s
    JOIN course c ON s.course_id = c.course_id
    LEFT JOIN evaluation e ON s.section_id = e.section_id
    WHERE s.year = %s
      AND s.semester = %s
    """
    cursor.execute(stmt, (semester_year, semester_term))
    rows = cursor.fetchall()

    conn.close()
    return rows


def page():
    rows = []
    all_sections = []

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

    all_sections_columns = [
        {"name": "section_id", "field": "section_id", "label": "Section ID"},
        {"name": "course_name", "field": "course_name", "label": "Course Name"},
        {"name": "semester_term", "field": "semester_term", "label": "Semester"},
        {"name": "semester_year", "field": "semester_year", "label": "Year"},
        {
            "name": "evaluation_status",
            "field": "evaluation_status",
            "label": "Evaluation Status",
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

    async def list_all_sections_with_status():
        if not (semester_year_all_input.value and semester_term_all_input.value):
            ui.notify(
                "Both Semester Year and Semester Term are required!", color="negative"
            )
            return

        try:
            nonlocal all_sections

            semester_year = int(semester_year_all_input.value)
            semester_term = semester_term_all_input.value

            all_sections = get_all_sections_with_evaluation_status(
                semester_year, semester_term
            )
            all_sections_table.rows = all_sections
            ui.notify(
                "Sections with evaluation status retrieved successfully!",
                color="positive",
            )
        except Exception as e:
            ui.notify(f"Error: {e}", color="negative")

    # Input Fields for Filtering Sections
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

    # Input Fields for Listing Sections with Evaluation Status
    with ui.row().classes("items-left mt-8"):
        semester_year_all_input = ui.input(
            "Semester Year", placeholder="Enter Year (e.g., 2024)"
        ).classes("w-48")
        semester_term_all_input = ui.select(
            ["SP", "SM", "FA"], label="Semester"
        ).classes("w-48")

        ui.button(
            "List All Sections with Status", on_click=list_all_sections_with_status
        )

    all_sections_table = ui.table(
        rows=all_sections,
        columns=all_sections_columns,
        column_defaults={"align": "left", "headerClasses": "uppercase text-primary"},
    )

from nicegui import ui
from TeamProject.Utilities import MySql


def get_data(course_id=None, start_semester=None, end_semester=None):
    conn = MySql.create_conn()
    cursor = conn.cursor(dictionary=True)

    # Base query to fetch sections
    stmt = """
    SELECT 
        s.section_id,
        s.semester,
        s.year,
        c.course_id,
        c.name AS course_name,
        s.student_enrolled
    FROM section s
    JOIN course c ON c.course_id = s.course_id
    """

    # Add filters for course and semester range
    conditions = []
    params = []

    if course_id:
        conditions.append("c.course_id = %s")
        params.append(course_id)

    if start_semester and end_semester:
        conditions.append("""
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
        """)
        start_year, start_sem = int(start_semester[:4]), start_semester[4:]
        end_year, end_sem = int(end_semester[:4]), end_semester[4:]
        params.extend([start_year, start_sem, end_year, end_sem])

    if conditions:
        stmt += " WHERE " + " AND ".join(conditions)

    cursor.execute(stmt, params)
    rows = cursor.fetchall()

    conn.close()
    return rows


def page():

    rows = get_data()  # Load all courses initially
    current_filter = ui.label('Currently showing all sections.')  # Default label

    columns = [
        {"name": "section_id", "field": "section_id", "label": "Section ID"},
        {"name": "semester", "field": "semester", "label": "Semester"},
        {"name": "year", "field": "year", "label": "Year"},
        {"name": "course_id", "field": "course_id", "label": "Course ID"},
        {"name": "course_name", "field": "course_name", "label": "Course Name"},
        {"name": "student_enrolled", "field": "student_enrolled", "label": "Students Enrolled"},
    ]

    async def filter_sections():
        with ui.dialog() as dialog, ui.card():
            inputs = {
                "Course ID": ui.input(label="Course ID (e.g., CS7330)"),
                "Start Semester": ui.input(label="Start Semester (e.g., 2023SP)"),
                "End Semester": ui.input(label="End Semester (e.g., 2024FA)"),
            }

            with ui.row():
                ui.button(
                    "Update",
                    on_click=lambda: dialog.submit(
                        {
                            "course_id": inputs["Course ID"].value,
                            "start": inputs["Start Semester"].value,
                            "end": inputs["End Semester"].value,
                        }
                    ),
                )
                ui.button("Cancel", on_click=lambda: dialog.close())

        result = await dialog
        if result:
            filtered_rows = get_data(result["course_id"], result["start"], result["end"])
            rows.clear()
            rows.extend(filtered_rows)
            table.update()

            # Update the filter label
            course_id = result["course_id"] or "all courses"
            start_semester = result["start"] or "all semesters"
            end_semester = result["end"] or "all semesters"
            current_filter.text = (
                f"Currently showing sections for course: {course_id}, "
                f"between {start_semester} and {end_semester}."
            )

    def reset_filter():
        rows.clear()
        rows.extend(get_data())  # Reload all courses
        table.update()
        current_filter.text = "Currently showing all sections."  # Reset label

    with ui.row().classes("items-left"):
        ui.button("Filter Sections", on_click=filter_sections)
        ui.button("Reset Filter", on_click=reset_filter)

    # Display current filter above the table
    current_filter.classes('text-lg font-bold text-primary')
    
    table = ui.table(
        rows=rows,
        columns=columns,
        column_defaults={"align": "left", "headerClasses": "uppercase text-primary"},
    )

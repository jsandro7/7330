import re
from nicegui import ui

# Validation functions
def validate_non_empty(entry):
    return entry.value.strip() != ""

def validate_degree_name(entry):
    return entry.value.strip() != ""

def validate_degree_level(entry):
    return entry.value.strip() != ""

def validate_course_id(entry):
    print(entry.value)
    return bool(re.match(r'^[a-zA-Z]{2,4}\d{4}$', entry.value.strip()))

def validate_course_name(entry):
    print(entry.value)
    return entry.value.strip() != ""

def validate_instructor_id(entry):
    return bool(re.match(r'^\d{8}$', entry.value.strip()))

def validate_instructor_name(entry):
    return entry.value.strip() != ""

def validate_section_id(entry):
    return entry.value.strip().isdigit() and len(entry.value.strip()) <= 3

def validate_semester(entry):
    return bool(re.match(r'^(FA|SP|SM)$', entry.value.strip()))

def validate_year(entry):
    year = entry.value.strip()
    return (
        year != "" and
        len(year) == 5 and
        year[:2].isdigit() and
        year[3:5].isdigit() and
        year[2] == "-"
    )

def validate_student_enrolled(entry):
    return entry.value.strip().isdigit()

def validate_code(entry):
    return len(entry.value.strip()) == 4

def validate_goal_description(entry):
    return entry.value.strip() != ""

def validate_evaluation_method(entry):
    return entry.value.strip() != ""

validation_functions = {
    "Degree Name": validate_degree_name,
    "Degree Level": validate_degree_level,
    "Course ID": validate_course_id,
    "Course Name": validate_course_name,
    "Instructor ID": validate_instructor_id,
    "Instructor Name": validate_instructor_name,
    "Section ID": validate_section_id,
    "Semester": validate_semester,
    "Year": validate_year,
    "Student Enrolled": validate_student_enrolled,
    "Code": validate_code,
    "Goal Description": validate_goal_description,
    "Evaluation Method": validate_evaluation_method
}

def check_entries(ui, entries):
    """Validate all entries and enable/disable the submit button."""
    all_valid = True
    for field, entry in entries.items():
        is_valid = validate_non_empty(entry) and validation_functions.get(field, lambda e: True)(ui, entry)
        if not is_valid:
            ui.notify(f'Formatting issue with {field}')
        all_valid &= is_valid
    
    return all_valid

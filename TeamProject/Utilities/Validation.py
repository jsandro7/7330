import re
from nicegui import ui

# Validation functions
def validate_non_empty(entry):
    return entry.strip() != ""

def validate_degree_name(entry):
    return entry.strip() != ""

def validate_degree_level(entry):
    return entry.strip() != ""

def validate_course_id(entry):
    return bool(re.match(r'^[a-zA-Z]{2,4}\d{4}$', entry.strip()))

def validate_course_name(entry):
    return entry.strip() != ""

def validate_instructor_id(entry):
    return bool(re.match(r'^\d{8}$', entry.strip()))

def validate_instructor_name(entry):
    return entry.strip() != ""

def validate_section_id(entry):
    return entry.strip().isdigit() and len(entry.strip()) <= 3

def validate_semester(entry):
    return bool(re.match(r'^(FA|SP|SM)$', entry.strip()))

def validate_year(entry):
    year = entry.strip()
    return (
        year != "" and
        len(year) == 5 and
        year[:2].isdigit() and
        year[3:5].isdigit() and
        year[2] == "-"
    )

def validate_student_enrolled(entry):
    return entry.strip().isdigit()

def validate_code(entry):
    return len(entry.strip()) == 4

def validate_goal_description(entry):
    return entry.strip() != ""

def validate_evaluation_method(entry):
    return entry.strip() != ""

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

def check_entries(entries):
    """Validate all entries and enable/disable the submit button."""
    all_valid = True
    for field, entry in entries.items():
        is_valid = validate_non_empty(entry) and validation_functions.get(field, lambda e: True)(entry)
        all_valid &= is_valid
    
    return all_valid
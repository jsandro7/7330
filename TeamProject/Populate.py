from TeamProject.Utilities import MySql
import random

def add_degree(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO degree
    (
        name,
        level
    )
    VALUES (%s, %s)   
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def add_course(args):
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

def add_instructor(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO instructor
    (
        id,
        name
    )
    VALUES (%s, %s)   
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def add_instructor(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO goal
    (
        code,
        name,
        level,
        description
    )
    VALUES (%s, %s, %s, %s)   
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def add_degree_course(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO degree_course
    (
        name,
        level,
        course_id
    )
    VALUES (%s, %s, %s)   
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def add_section(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO section
    (
        section_id,
        course_id,
        semester,
        year,
        student_enrolled
    )
    VALUES (%s, %s, %s)   
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def add_teaches(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO teaches
    (
        section_id,
        course_id,
        id
    )
    VALUES (%s, %s, %s)   
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def add_evaluation(args):
    conn = MySql.create_conn()
    cursor = conn.cursor()

    stmt = """
    INSERT INTO evaluation
    (
        section_id,
        code,
        evaluation_method,
        comment,
        A_count,
        B_count,
        C_count,
        F_count
    )
    VALUES (%s, %s, %s)   
    """

    cursor.execute(stmt, args)
    conn.commit()
    conn.close()

def initialize_db():
    # Degree
    degrees = [
        ['Finance', 'BA'],
        ['Accounting', 'BA'],
        ['Computer Science', 'BA'],
        ['Computer Engineering', 'BA'],
        ['Data Science', 'BA'],
    ]

    for degree in degrees:
        add_degree(degree[0], degree[1])

    # Course
    courses = [
        ['FIN1000', 'Intro Finance'],
        ['FIN2000', 'Intermediate Finance'],
        ['FIN3000', 'Advanced Finance'],
        ['ACCT1000', 'Intro Finance'],
        ['ACCT2000', 'Intermediate Finance'],
        ['ACCT3000', 'Advanced Finance'],
        ['CS1000', 'Intro Computer Science'],
        ['CS2000', 'Intermediate Computer Science'],
        ['CS3000', 'Advanced Computer Science'],
        ['CSE1000', 'Intro Computer Engineering'],
        ['CSE2000', 'Intermediate Computer Engineering'],
        ['CSE3000', 'Advanced Computer Engineering'],
        ['DS1000', 'Intro Data Science'],
        ['DS2000', 'Intermediate Data Science'],
        ['DS3000', 'Advanced Data Science'],
    ]

    # Degree-Course
    for course in courses:
        add_course(course[0], course[1])
        add_degree_course(course[1].split(' ')[1:].join(' '), 'BA', course[0])

    # Instructor
    instructors = [
        ['10000001', 'Thomas Barry'],
        ['10000002', 'Amy Altizer'],
        ['20000001', 'Frank Coyle'],
        ['20000002', 'Theodore Manikas'],
        ['20000003', 'Qiguo Jing']
    ]

    for instructor in instructors:
        add_instructor(instructor[0], instructor[1])

    # Section
    semester = ["FA", "SP", "SM"]
    year = [2021, 2022, 2023, 2024, 2025]
    for course in courses:
        for i in range(0, 51, 10):
            section_id = int(random() * 10) + i
            sem = semester[int(random() * 3)]
            yr = year[int(random() * 5)]
            course_id = course[0]
            numstudents = int(random() * 50)
            add_section(section_id, course_id, sem, yr, numstudents)
            # Teaches
            add_teaches(section_id, course_id, instructors[random() * 5][0])

    # Goal

    # Evaluation
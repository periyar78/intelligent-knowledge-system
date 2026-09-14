"""
A few hand-written convenience queries (optional to use directly;
the agent will mostly generate its own SQL via the mysql_tool).
"""
from mysql_db.connection import run_query


def get_student_by_name(name: str):
    return run_query(f"SELECT * FROM Student WHERE name = '{name}';")


def get_students_by_department_gpa(department: str, min_gpa: float):
    return run_query(
        f"SELECT student_id, name, gpa FROM Student "
        f"WHERE department = '{department}' AND gpa > {min_gpa};"
    )


def get_all_students():
    return run_query("SELECT * FROM Student;")


def get_schema_description():
    """
    Returns a human-readable schema summary — very useful to feed into
    the LLM's system prompt so it can write correct SQL.
    """
    return """
Tables:

Student(student_id INT, name VARCHAR, department VARCHAR, gpa DECIMAL, year_joined INT)
Department(dept_id INT, dept_name VARCHAR)
Faculty(faculty_id INT, name VARCHAR, specialization VARCHAR)
Course(course_id INT, course_name VARCHAR, faculty_id INT, dept_id INT)
Enrollment(enrollment_id INT, student_id INT, course_id INT)

Relationships:
- Enrollment.student_id -> Student.student_id
- Enrollment.course_id  -> Course.course_id
- Course.faculty_id     -> Faculty.faculty_id
- Course.dept_id        -> Department.dept_id
"""

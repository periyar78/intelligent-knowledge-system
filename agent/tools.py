import json
from functools import lru_cache

import chromadb
import mysql.connector
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from langchain_core.tools import tool


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "sabari@29",
    "database": "university"
}

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "sabari@29"


# ============================================================
# EMBEDDING MODEL
# Loaded only once
# ============================================================

@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


# ============================================================
# MYSQL HELPER
# ============================================================

def run_mysql_query(query, params=None):
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)

        cursor = connection.cursor(dictionary=True)

        cursor.execute(query, params or ())

        rows = cursor.fetchall()

        return rows

    except mysql.connector.Error as e:
        return {
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# ============================================================
# MYSQL TOOL 1
# ============================================================

@tool
def get_student_gpa(student_name: str) -> str:
    """
    Get the GPA of a student.

    Use this for questions asking for a student's GPA,
    academic score, or performance.

    Example:
    get_student_gpa("Arun")
    """

    query = """
        SELECT
            student_id,
            student_name,
            gpa
        FROM students
        WHERE LOWER(student_name) = LOWER(%s)
    """

    result = run_mysql_query(query, (student_name,))

    return json.dumps(result, default=str)


# ============================================================
# MYSQL TOOL 2
# ============================================================

@tool
def count_students_by_department(department_name: str) -> str:
    """
    Count the number of students in a department.

    Example:
    count_students_by_department("CSE")
    """

    query = """
        SELECT
            d.department_name,
            COUNT(s.student_id) AS student_count
        FROM departments d
        LEFT JOIN students s
            ON d.department_id = s.department_id
        WHERE LOWER(d.department_name) = LOWER(%s)
        GROUP BY d.department_id, d.department_name
    """

    result = run_mysql_query(query, (department_name,))

    return json.dumps(result, default=str)


# ============================================================
# MYSQL TOOL 3
# ============================================================

@tool
def get_students_by_gpa(min_gpa: float = None, max_gpa: float = None) -> str:
    """
    Find students using GPA limits.

    Use this for questions such as:
    - students with GPA above 8
    - students below GPA 7
    - students between GPA 7 and 9

    Provide min_gpa or max_gpa as needed.
    """

    if min_gpa is not None and max_gpa is not None:

        query = """
            SELECT
                student_id,
                student_name,
                department_id,
                gpa
            FROM students
            WHERE gpa >= %s
              AND gpa <= %s
            ORDER BY gpa DESC
        """

        result = run_mysql_query(
            query,
            (min_gpa, max_gpa)
        )

    elif min_gpa is not None:

        query = """
            SELECT
                student_id,
                student_name,
                department_id,
                gpa
            FROM students
            WHERE gpa >= %s
            ORDER BY gpa DESC
        """

        result = run_mysql_query(
            query,
            (min_gpa,)
        )

    elif max_gpa is not None:

        query = """
            SELECT
                student_id,
                student_name,
                department_id,
                gpa
            FROM students
            WHERE gpa <= %s
            ORDER BY gpa DESC
        """

        result = run_mysql_query(
            query,
            (max_gpa,)
        )

    else:

        query = """
            SELECT
                student_id,
                student_name,
                department_id,
                gpa
            FROM students
            ORDER BY gpa DESC
        """

        result = run_mysql_query(query)

    return json.dumps(result, default=str)


# ============================================================
# MYSQL TOOL 4
# ============================================================

@tool
def get_all_students(department_name: str = None) -> str:
    """
    Get student records.

    Optionally filter by department.

    Example:
    get_all_students("CSE")
    """

    if department_name:

        query = """
            SELECT
                s.student_id,
                s.student_name,
                d.department_name,
                s.gpa
            FROM students s
            JOIN departments d
                ON s.department_id = d.department_id
            WHERE LOWER(d.department_name) = LOWER(%s)
            ORDER BY s.student_id
        """

        result = run_mysql_query(
            query,
            (department_name,)
        )

    else:

        query = """
            SELECT
                s.student_id,
                s.student_name,
                d.department_name,
                s.gpa
            FROM students s
            JOIN departments d
                ON s.department_id = d.department_id
            ORDER BY s.student_id
        """

        result = run_mysql_query(query)

    return json.dumps(result, default=str)


# ============================================================
# CHROMADB TOOL
# ============================================================

@tool
def semantic_policy_search(query: str) -> str:
    """
    Search university policy documents using semantic similarity.

    Use this for:
    attendance policies, exam rules, library rules,
    hostel rules, academic regulations and other
    textual university information.
    """

    try:

        client = chromadb.PersistentClient(
            path="chroma_data"
        )

        collection = client.get_collection(
            name="university_docs"
        )

        model = get_embedding_model()

        embedding = model.encode(
            [query]
        ).tolist()

        results = collection.query(
            query_embeddings=embedding,
            n_results=3
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        output = []

        for i, document in enumerate(documents):

            source = (
                metadatas[i].get("source")
                if i < len(metadatas)
                else "unknown"
            )

            output.append(
                {
                    "source": source,
                    "content": document
                }
            )

        return json.dumps(
            output,
            indent=2
        )

    except Exception as e:

        return json.dumps(
            {
                "error": str(e)
            }
        )


# ============================================================
# NEO4J HELPER
# ============================================================

def run_neo4j_query(query, params=None):
    driver = None

    try:

        driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(
                NEO4J_USER,
                NEO4J_PASSWORD
            )
        )

        with driver.session() as session:

            result = session.run(
                query,
                params or {}
            )

            return [
                record.data()
                for record in result
            ]

    except Exception as e:

        return {
            "error": str(e)
        }

    finally:

        if driver:
            driver.close()


# ============================================================
# NEO4J TOOL 1
# ============================================================

@tool
def find_course_teacher(course_name: str) -> str:
    """
    Find the faculty member who teaches a course.

    Example:
    find_course_teacher("Machine Learning")
    """

    query = """
        MATCH (f:Faculty)-[:TEACHES]->(c:Course)
        WHERE toLower(c.name) = toLower($course_name)
        RETURN
            f.name AS faculty,
            c.name AS course
    """

    result = run_neo4j_query(
        query,
        {
            "course_name": course_name
        }
    )

    return json.dumps(result)


# ============================================================
# NEO4J TOOL 2
# ============================================================

@tool
def find_ai_specialized_faculty() -> str:
    """
    Find faculty members who specialize in
    Artificial Intelligence.
    """

    query = """
        MATCH (f:Faculty)
        WHERE toLower(f.specialization)
              CONTAINS 'artificial intelligence'
        RETURN
            f.name AS faculty,
            f.specialization AS specialization
        ORDER BY f.name
    """

    result = run_neo4j_query(query)

    return json.dumps(result)


# ============================================================
# NEO4J TOOL 3
# ============================================================

@tool
def find_students_in_ai_faculty_courses() -> str:
    """
    Find students enrolled in courses taught by
    faculty who specialize in Artificial Intelligence.
    """

    query = """
        MATCH
            (s:Student)-[:ENROLLED_IN]->(c:Course),
            (f:Faculty)-[:TEACHES]->(c)

        WHERE toLower(f.specialization)
              CONTAINS 'artificial intelligence'

        RETURN
            s.id AS student_id,
            s.name AS student,
            s.gpa AS gpa,
            c.name AS course,
            f.name AS faculty,
            f.specialization AS specialization

        ORDER BY s.gpa DESC
    """

    result = run_neo4j_query(query)

    return json.dumps(result)


# ============================================================
# NEO4J TOOL 4
# ============================================================

@tool
def find_students_in_course(course_name: str) -> str:
    """
    Find students enrolled in a particular course.

    Example:
    find_students_in_course("Machine Learning")
    """

    query = """
        MATCH (s:Student)-[:ENROLLED_IN]->(c:Course)
        WHERE toLower(c.name) = toLower($course_name)
        RETURN
            s.id AS student_id,
            s.name AS student,
            s.gpa AS gpa,
            c.name AS course
        ORDER BY s.gpa DESC
    """

    result = run_neo4j_query(
        query,
        {
            "course_name": course_name
        }
    )

    return json.dumps(result)


# ============================================================
# ALL TOOLS
# ============================================================

ALL_TOOLS = [
    get_student_gpa,
    count_students_by_department,
    get_students_by_gpa,
    get_all_students,

    semantic_policy_search,

    find_course_teacher,
    find_ai_specialized_faculty,
    find_students_in_ai_faculty_courses,
    find_students_in_course
]
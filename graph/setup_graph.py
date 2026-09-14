from neo4j import GraphDatabase

# -----------------------------
# Neo4j connection details
# -----------------------------

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "sabari@29"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


# -----------------------------
# Create university graph
# -----------------------------

def create_graph():
    with driver.session() as session:

        # Clear old data
        session.run("MATCH (n) DETACH DELETE n")

        # -------------------------
        # Departments
        # -------------------------

        session.run("""
        CREATE
        (:Department {id: 1, name: 'CSE'}),
        (:Department {id: 2, name: 'IT'}),
        (:Department {id: 3, name: 'ECE'}),
        (:Department {id: 4, name: 'MECH'})
        """)

        # -------------------------
        # Students
        # -------------------------

        students = [
            (101, "Arun", 8.50),
            (102, "Priya", 9.10),
            (103, "Rahul", 7.80),
            (104, "Divya", 8.90),
            (105, "Karthik", 7.20),
            (106, "Sneha", 8.30),
            (107, "Vijay", 6.80),
            (108, "Anitha", 8.10),
            (109, "Rohit", 9.20),
            (110, "Meena", 6.50),
            (111, "Sanjay", 7.90),
            (112, "Pooja", 8.70),
            (113, "Ajay", 7.40),
            (114, "Nisha", 9.00),
            (115, "Manoj", 6.90)
        ]

        for student_id, name, gpa in students:
            session.run("""
            MATCH (d:Department {id: $department_id})
            CREATE (s:Student {
                id: $student_id,
                name: $name,
                gpa: $gpa
            })
            CREATE (s)-[:BELONGS_TO]->(d)
            """,
            student_id=student_id,
            name=name,
            gpa=gpa,
            department_id=1 if student_id in [101,103,104,107,109,112] else
                            2 if student_id in [102,106,110,114] else
                            3 if student_id in [105,111,115] else
                            4)

        # -------------------------
        # Faculty
        # -------------------------

        faculty = [
            (201, "Dr. Kumar", "Artificial Intelligence"),
            (202, "Dr. Ravi", "Machine Learning"),
            (203, "Dr. Priya", "Database Systems"),
            (204, "Dr. Meena", "Computer Networks"),
            (205, "Dr. Suresh", "Embedded Systems")
        ]

        faculty_departments = {
            201: 1,
            202: 1,
            203: 2,
            204: 2,
            205: 3
        }

        for faculty_id, name, specialization in faculty:
            session.run("""
            MATCH (d:Department {id: $department_id})
            CREATE (f:Faculty {
                id: $faculty_id,
                name: $name,
                specialization: $specialization
            })
            CREATE (f)-[:BELONGS_TO]->(d)
            """,
            faculty_id=faculty_id,
            name=name,
            specialization=specialization,
            department_id=faculty_departments[faculty_id])

        # -------------------------
        # Courses
        # -------------------------

        courses = [
            (301, "Artificial Intelligence", 1, 201),
            (302, "Machine Learning", 1, 202),
            (303, "Database Management Systems", 2, 203),
            (304, "Computer Networks", 2, 204),
            (305, "Embedded Systems", 3, 205),
            (306, "Data Structures", 1, 202),
            (307, "Deep Learning", 1, 201)
        ]

        for course_id, course_name, department_id, faculty_id in courses:
            session.run("""
            MATCH (d:Department {id: $department_id})
            MATCH (f:Faculty {id: $faculty_id})

            CREATE (c:Course {
                id: $course_id,
                name: $course_name
            })

            CREATE (c)-[:BELONGS_TO]->(d)
            CREATE (f)-[:TEACHES]->(c)
            """,
            course_id=course_id,
            course_name=course_name,
            department_id=department_id,
            faculty_id=faculty_id)

        # -------------------------
        # Student enrollments
        # -------------------------

        enrollments = [
            (101, 301),
            (101, 302),
            (102, 303),
            (103, 302),
            (104, 301),
            (104, 307),
            (105, 305),
            (106, 303),
            (107, 302),
            (108, 305),
            (109, 301),
            (109, 307),
            (112, 302),
            (112, 306),
            (114, 303),
            (115, 305)
        ]

        for student_id, course_id in enrollments:
            session.run("""
            MATCH (s:Student {id: $student_id})
            MATCH (c:Course {id: $course_id})
            CREATE (s)-[:ENROLLED_IN]->(c)
            """,
            student_id=student_id,
            course_id=course_id)

    print("University graph created successfully!")


# -----------------------------
# Run
# -----------------------------

try:
    create_graph()
finally:
    driver.close()
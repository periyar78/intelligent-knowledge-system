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
# Query: Who teaches a course?
# -----------------------------

def find_course_teacher(course_name):
    query = """
    MATCH (f:Faculty)-[:TEACHES]->(c:Course)
    WHERE c.name = $course_name
    RETURN f.name AS faculty, c.name AS course
    """

    with driver.session() as session:
        result = session.run(
            query,
            course_name=course_name
        )

        records = list(result)

        if not records:
            print("No faculty found for this course.")
            return

        for record in records:
            print(
                f"Course: {record['course']}"
            )
            print(
                f"Faculty: {record['faculty']}"
            )


# -----------------------------
# Main program
# -----------------------------

try:
    course = input("Enter course name: ")

    find_course_teacher(course)

finally:
    driver.close()
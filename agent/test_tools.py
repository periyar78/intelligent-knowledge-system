from agent.tools import mysql_tool, vector_tool, neo4j_tool


print("\n==============================")
print("TEST 1: MYSQL")
print("==============================")

result = mysql_tool.invoke(
    "What is Arun's GPA?"
)

print(result)


print("\n==============================")
print("TEST 2: VECTOR SEARCH")
print("==============================")

result = vector_tool.invoke(
    "What is the minimum attendance required for exams?"
)

print(result)


print("\n==============================")
print("TEST 3: NEO4J")
print("==============================")

result = neo4j_tool.invoke(
    "Who teaches Machine Learning?"
)

print(result)
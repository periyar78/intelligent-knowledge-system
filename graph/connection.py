"""
Neo4j connection + Cypher execution helper.
"""
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")

_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def run_cypher(query: str, parameters: dict = None):
    """
    Run a Cypher query and return results as a list of dicts.
    """
    with _driver.session() as session:
        result = session.run(query, parameters or {})
        return [record.data() for record in result]


def close_driver():
    _driver.close()


if __name__ == "__main__":
    # Quick standalone test (run graph/setup_graph.py first)
    print(run_cypher("MATCH (s:Student) RETURN s.name LIMIT 5;"))

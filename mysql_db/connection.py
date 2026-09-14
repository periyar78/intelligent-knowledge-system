"""
MySQL connection + query execution helper.
"""
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "university")


def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
    )


def run_query(sql: str):
    """
    Run a SQL query and return results as a list of dicts.
    Only SELECT queries should be passed here in the agent context
    (write access is intentionally not exposed to the LLM).
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql)
        if cursor.with_rows:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = {"rows_affected": cursor.rowcount}
    finally:
        cursor.close()
        conn.close()
    return result


if __name__ == "__main__":
    # Quick standalone test
    print(run_query("SELECT * FROM Student LIMIT 5;"))

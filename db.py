"""
Database access layer for GenAI SQL.
Handles the PostgreSQL connection, schema introspection (used to give the
LLM context about the tables it can query), and query execution.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "genai_sql_demo"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )


def get_schema_description():
    """
    Introspects the connected database and returns a human-readable
    description of every table and column. This text is fed to the LLM
    so generated SQL references real table/column names.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                ORDER BY table_name, ordinal_position;
                """
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    schema = {}
    for table_name, column_name, data_type in rows:
        schema.setdefault(table_name, []).append(f"{column_name} ({data_type})")

    lines = []
    for table, columns in schema.items():
        lines.append(f"Table: {table}\n  Columns: " + ", ".join(columns))
    return "\n".join(lines)


def execute_query(sql):
    """
    Executes a SQL statement. Returns a list of dict rows for SELECT-type
    queries, or a status message dict for INSERT/UPDATE/DELETE/DDL.
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            if cur.description:
                rows = cur.fetchall()
                conn.commit()
                return [dict(row) for row in rows]
            conn.commit()
            return {"message": f"Query executed successfully. Rows affected: {cur.rowcount}"}
    finally:
        conn.close()

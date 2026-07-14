"""
GenAI SQL - Natural Language to PostgreSQL Query Generator
CLI entry point. Reads a plain-English question, converts it to SQL via
Gemini, and executes it against the connected PostgreSQL database.
"""

import sys
from db import execute_query, get_schema_description
from query_generator import generate_sql

DESTRUCTIVE_KEYWORDS = ("DELETE", "DROP", "UPDATE", "TRUNCATE", "ALTER", "INSERT")


def is_destructive(sql):
    upper_sql = sql.upper()
    return any(keyword in upper_sql for keyword in DESTRUCTIVE_KEYWORDS)


def confirm_if_destructive(sql):
    if is_destructive(sql):
        print(f"\n\u26a0  This query will modify data:\n  {sql}")
        choice = input("Proceed? (y/n): ").strip().lower()
        return choice == "y"
    return True


def print_results(results):
    if isinstance(results, dict):
        print(results["message"])
        return
    if not results:
        print("No rows returned.")
        return
    headers = list(results[0].keys())
    col_widths = {h: max(len(str(h)), max(len(str(row[h])) for row in results)) for h in headers}
    header_line = " | ".join(h.ljust(col_widths[h]) for h in headers)
    print(header_line)
    print("-" * len(header_line))
    for row in results:
        print(" | ".join(str(row[h]).ljust(col_widths[h]) for h in headers))


def main():
    print("=== GenAI SQL: Natural Language to PostgreSQL Query Generator ===")
    print("Type a question in plain English (or 'exit' to quit).\n")

    try:
        schema = get_schema_description()
    except Exception as e:
        print(f"Could not connect to database: {e}")
        print("Make sure PostgreSQL is running and .env is configured correctly.")
        sys.exit(1)

    while True:
        question = input("\nAsk a question: ").strip()
        if question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not question:
            continue

        try:
            sql = generate_sql(question, schema)
        except Exception as e:
            print(f"Error generating SQL: {e}")
            continue

        print(f"\nGenerated SQL:\n  {sql}")

        if not confirm_if_destructive(sql):
            print("Query cancelled.")
            continue

        try:
            results = execute_query(sql)
            print("\nResults:")
            print_results(results)
        except Exception as e:
            print(f"Error executing query: {e}")


if __name__ == "__main__":
    main()

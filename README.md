# GenAI SQL – Natural Language to PostgreSQL Query Generator

Convert plain-English questions into PostgreSQL queries using Google's Gemini API, execute them against a live PostgreSQL database, and see results instantly from the command line.

## Features
- Translates natural language questions into syntactically valid PostgreSQL queries
- Automatically reads the connected database's schema and feeds it to the LLM as context, so generated queries reference real table/column names
- Executes generated SQL directly against PostgreSQL and prints formatted results
- Safety check — prompts for confirmation before running any query that modifies data (`INSERT` / `UPDATE` / `DELETE` / `DROP` / `ALTER` / `TRUNCATE`)
- Simple interactive CLI, no web server required
- Ships with a ready-to-use sample schema (employees/departments) so you can try it in minutes

## Tech Stack
- Python 3.9+
- PostgreSQL
- Google Gemini API (`google-generativeai`)
- psycopg2

## How It Works
1. On startup, the app introspects the connected PostgreSQL database (via `information_schema`) to build a text description of every table and column.
2. When you type a question, that schema description plus your question are sent to Gemini with a prompt engineered to return a single SQL statement and nothing else.
3. The response is cleaned (any stray markdown fences stripped) and, if it looks like a write operation, you're asked to confirm before it runs.
4. The query is executed with `psycopg2` and results are printed as a formatted table.

## Project Structure
```
genai-sql-query-generator/
├── main.py              # CLI entry point / REPL loop
├── db.py                 # PostgreSQL connection, schema introspection, query execution
├── query_generator.py    # Gemini prompt construction and SQL generation
├── schema.sql             # Sample schema + seed data (employees/departments)
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. Clone the repo and install dependencies:
   ```bash
   git clone https://github.com/Srinivas-kalikiri/genai-sql-query-generator.git
   cd genai-sql-query-generator
   pip install -r requirements.txt
   ```

2. Create a PostgreSQL database and load the sample schema:
   ```bash
   createdb genai_sql_demo
   psql -d genai_sql_demo -f schema.sql
   ```

3. Copy `.env.example` to `.env` and fill in your database credentials and [Gemini API key](https://ai.google.dev/):
   ```bash
   cp .env.example .env
   ```

4. Run the app:
   ```bash
   python main.py
   ```

## Example Session
```
=== GenAI SQL: Natural Language to PostgreSQL Query Generator ===
Type a question in plain English (or 'exit' to quit).

Ask a question: Show me all employees in the Engineering department earning more than 80000

Generated SQL:
  SELECT e.first_name, e.last_name, e.salary FROM employees e JOIN departments d ON e.department_id = d.department_id WHERE d.department_name = 'Engineering' AND e.salary > 80000;

Results:
first_name | last_name | salary
---------- | --------- | --------
Ananya     | Sharma    | 85000.00
Rohit      | Verma     | 92000.00
```

## Possible Improvements
- Multi-turn conversation context for follow-up questions
- Cache the schema description instead of re-querying it on every run
- A lightweight Flask/FastAPI wrapper for a browser-based UI
- Export query results to CSV

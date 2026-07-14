"""
Natural language -> SQL translation using the Google Gemini API.
Builds a schema-aware prompt so generated queries reference real
table/column names from the connected database.
"""

import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-1.5-flash"

PROMPT_TEMPLATE = """You are an expert PostgreSQL query generator.
Convert the user's natural language request into a single, valid, syntactically
correct PostgreSQL query.

Database schema:
{schema}

Rules:
- Output ONLY the SQL query. No explanations, no markdown formatting, no code fences.
- Use the exact table and column names given in the schema above.
- If the request is ambiguous, make the most reasonable assumption.
- Always end the query with a semicolon.
- Prefer SELECT queries unless the user explicitly asks to insert, update, or delete data.

User request: "{question}"

SQL query:"""


def clean_sql_response(text):
    """Strip markdown code fences and extra whitespace the model sometimes adds."""
    text = text.strip()
    text = re.sub(r"^```(sql)?", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"```$", "", text).strip()
    return text


def generate_sql(question, schema):
    model = genai.GenerativeModel(MODEL_NAME)
    prompt = PROMPT_TEMPLATE.format(schema=schema, question=question)
    response = model.generate_content(prompt)
    return clean_sql_response(response.text)

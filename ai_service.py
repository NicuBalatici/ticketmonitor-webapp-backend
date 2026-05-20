import os
from openai import AzureOpenAI

# Am adăugat instrucțiuni stricte (CRITICAL RULES) pentru a bloca orice variabilă
DB_SCHEMA = """You are a SQL Server expert. Generate SQL queries based on this schema:

Table: INCIDENT_TICKETS
- TICKET_NUMBER VARCHAR(50) PRIMARY KEY
- STATUS: 'Open', 'In Progress', 'Resolved', 'Closed', 'Waiting for Customer'
- PRIORITY: 'High', 'Medium', 'Low', 'Critical'
- COMPANY, PROJECT, TEAM, ASSIGNED_PERSON, SERVICE
- DESCRIPTION, NOTES, RESOLUTION
- CATEGORY_TIER_1, CATEGORY_TIER_2, CATEGORY_TIER_3
- SUBMIT_DATETIME, RESOLVED_DATETIME, CLOSED_DATETIME, LAST_MODIFIED_DATETIME
- Estimated_Resolution (SLA deadline - datetime when ticket should be resolved)
- PENDING_DURATION INT (minutes in pending)

CRITICAL RULES FOR DEMO:
1. NEVER use parameterized variables (like @AssignedPerson or ?). ALWAYS hardcode the values directly in the SQL string.
2. If the user asks about "their" tickets or uses first-person (e.g., "am", "mele", "my"), hardcode ASSIGNED_PERSON = 'Nicolae Balatici' in the query.
3. Return ONLY the raw SQL query. Absolutely no markdown backticks (like ```sql), no formatting, no explanations.
4. Use TOP instead of LIMIT.
"""

def get_sql_from_question(question: str) -> str:
    client = AzureOpenAI(
        api_key=os.environ["API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ["API_VERSION"],
    )

    response = client.chat.completions.create(
        model=os.environ["MODEL"],
        messages=[
            {"role": "system", "content": DB_SCHEMA},
            {"role": "user", "content": question},
        ],
    )

    # Scoatem eventualele spații sau caractere ciudate de la început/sfârșit
    return response.choices[0].message.content.strip()


def get_natural_response(question: str, sql_result: str) -> str:
    client = AzureOpenAI(
        api_key=os.environ["API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ["API_VERSION"],
    )

    response = client.chat.completions.create(
        model=os.environ["MODEL"],
        messages=[
            {"role": "system", "content": "You are a helpful assistant that explains SQL query results in natural language. Answer in Romanian. Give only a short, direct answer. Do not mention SQL, query results, or technical details. Do not use quotation marks around names or values."},
            {"role": "user", "content": f"Question: {question}\nSQL Result: {sql_result}"},
        ],
    )

    return response.choices[0].message.content.strip()
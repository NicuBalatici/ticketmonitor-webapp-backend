import os
from openai import AzureOpenAI

DB_SCHEMA = """You are a SQL Server expert. Generate SQL queries based on this schema:

Table: INCIDENT_TICKETS
- Ticket_Number VARCHAR(20) PRIMARY KEY
- Status: 'Open', 'In Progress', 'Resolved', 'Closed', 'Waiting for Customer'
- Priority: 'High', 'Medium', 'Low', 'Critical'
- Company, Project, Service VARCHAR(100)
- Team INT (references Teams.TeamID)
- Assigned_Person INT (references Users.UserID)
- Description, Notes, Resolution TEXT
- Cat_T1, Cat_T2, Cat_T3 VARCHAR(50)
- Submit_Datetime, Resolved_Datetime, Closed_Datetime, Last_Modified DATETIME
- Estimated_Resolution DATETIME (SLA deadline)
- Pending_Duration INT (minutes in pending)

Table: Teams
- TeamID INT PRIMARY KEY
- TeamName VARCHAR(50)

Table: Users
- UserID INT PRIMARY KEY
- FullName VARCHAR(100)
- Email VARCHAR(100)
- Team INT (references Teams.TeamID)

Table: Conversations
- ConversationID INT PRIMARY KEY
- UserID INT
- Ticket VARCHAR(20)

Table: Messages
- MessageID INT PRIMARY KEY
- ConversationID INT
- SenderRole VARCHAR(20)
- Message VARCHAR(MAX)
- Sent_Datetime DATETIME

Rules:
- Use TOP instead of LIMIT
- SLA breach: Estimated_Resolution < GETDATE() AND Status NOT IN ('Resolved','Closed')
- Average resolution time: DATEDIFF(minute, Submit_Datetime, Resolved_Datetime)
- For team names, JOIN with Teams table: JOIN Teams t ON t.TeamID = INCIDENT_TICKETS.Team
- For person names, JOIN with Users table: JOIN Users u ON u.UserID = INCIDENT_TICKETS.Assigned_Person
- Return ONLY the SQL query, no markdown, no explanations."""

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
            {"role": "system", "content": "You are a helpful assistant that explains SQL query results in natural language. Answer in Romanian.Give only a short, direct answer. Do not mention SQL, query results, or technical details.Do not use quotation marks around names or values."},
            {"role": "user", "content": f"Question: {question}\nSQL Result: {sql_result}"},
        ],

    )

    return response.choices[0].message.content.strip()
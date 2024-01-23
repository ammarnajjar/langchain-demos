from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI

model = 'luna-ai-llama2'
print(f'{model=}')

CONNECTION_STRING = "mssql+pyodbc://sa:mssql_1234@localhost:1433/Chinook?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"

db = SQLDatabase.from_uri(CONNECTION_STRING,
    include_tables=["Employee"],  # save tokens in the prompt
    sample_rows_in_table_info=100,
)

llm = ChatOpenAI(model=model, temperature=0)
chain = create_sql_query_chain(llm, db)

response = chain.invoke({"question": "How many employees are there"})
print(response)


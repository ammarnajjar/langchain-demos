from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from operator import itemgetter

model = 'ggml-gpt4all-j'
print(f'{model=}')

CONNECTION_STRING = "mssql+pyodbc://sa:mssql_1234@localhost:1433/Chinook?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"

db = SQLDatabase.from_uri(CONNECTION_STRING,
    include_tables=["Employee"],  # save tokens in the prompt
    sample_rows_in_table_info=100,
)

llm = ChatOpenAI(model=model, temperature=0)
write_query = create_sql_query_chain(llm, db)
execute_query = QuerySQLDataBaseTool(db=db)

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=(itemgetter("query") | execute_query)
    )
    | answer
)

response = chain.invoke({"question": "How many employee are there"})
print(response)


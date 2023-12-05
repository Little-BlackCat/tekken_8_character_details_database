from sqlalchemy import create_engine
from extract_data import extract_data
from sqlalchemy import create_engine
from airflow.models import Variable

# Connection details
host = Variable.get("HOST")
username = Variable.get("USERNAME")
password = Variable.get("PASSWORD")
database = Variable.get("DATABASE")

def scrap_data_from_web():
  '''The function scrap_data_from_web scrapes data from a website, connects to a PostgreSQL database,
  writes the data to a table, and adds a primary key constraint to the table.

  '''

  # Check if any of the required environment variables is None
  if None in (host, username, password, database):
    raise ValueError("One or more required environment variables are not set.")

  # Database connection details
  database_url = f'postgresql://{username}:{password}@{host}:5432/{database}'
  engine = create_engine(database_url)

  # Write the DataFrame to the table
  df = extract_data()
  df.to_sql('tekken_8_character_details', con=engine, if_exists='replace', index=True, schema='public')
  
  # Execute SQL command to add primary key constraint
  with engine.connect() as con:
    con.execute('ALTER TABLE tekken_8_character_details ADD PRIMARY KEY ("id");')

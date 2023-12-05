from sqlalchemy import create_engine
from extract_data import extract_data
from sqlalchemy import create_engine
from dotenv import load_dotenv
from airflow.models import Variable

# Connection details
host = Variable.get("HOST")
username = Variable.get("USERNAME")
password = Variable.get("PASSWORD")
database = Variable.get("DATABASE")

def scrap_data_from_web():
  # Check if any of the required environment variables is None
  if None in (host, username, password, database):
    raise ValueError("One or more required environment variables are not set.")

  # Replace these values with your actual database connection details
  database_url = f'postgresql://{username}:{password}@{host}:5432/{database}'
  print(f"Constructed database_url: {database_url}")

  engine = create_engine(database_url)

  df = extract_data()
  df.to_sql('tekken-8-character-details', con=engine, if_exists='replace', index=True)

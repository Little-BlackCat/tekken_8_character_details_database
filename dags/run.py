from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from database import scrap_data_from_web

def get_data_from_web():
  scrap_data_from_web()
  print("Load data to Supabase success.")


with DAG (

  "tekken_8_character_details_dag",
  start_date=days_ago(1),
  schedule_interval="@daily",
  default_args={
    'email': ["neko.sword@gmail.com"],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
  },
  tags=["tekken_8_character"]

) as dag:

  t1 = PythonOperator(
    task_id="get_data_from_web",
    python_callable=get_data_from_web,
  )

  t1 
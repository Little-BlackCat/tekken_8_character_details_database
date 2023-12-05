from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from database import scrap_data_from_web

def get_data_from_web():
  get_data_to_database = scrap_data_from_web()
  return get_data_to_database


with DAG(
  "tekken_8_character_details_dag",
  start_date=days_ago(1),
  schedule_interval="@daily",
  default_args={
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'catchup': False,  # Disable catching up to avoid running multiple times for past dates
    },
  tags=["tekken_8_character"]

) as dag:

  t1 = PythonOperator(
    task_id="get_data_from_web",
    python_callable=get_data_from_web,
  )

  t1 
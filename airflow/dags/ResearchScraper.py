from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 16),  # Start date of the DAG
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG object
dag = DAG(
    'research_scraper',  # DAG ID
    default_args=default_args,
    description='A simple DAG to run a task weekly',
    schedule_interval=timedelta(days=7),  # Run the DAG every week
)

# Define tasks
start_task = DummyOperator(task_id='start', dag=dag)

def my_python_function():
    # Write your Python code here
    print("Executing my weekly task")

research_scraper = PythonOperator(
    task_id='research_scraper',
    python_callable=my_python_function,
    dag=dag,
)

end_task = DummyOperator(task_id='end', dag=dag)

# Define task dependencies
start_task >> research_scraper >> end_task

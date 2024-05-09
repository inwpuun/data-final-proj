from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG('update_visualization', start_date=days_ago(1), schedule_interval='*/15 * * * *')

spark = BashOperator(task_id='run_spark', bash_command='python /opt/airflow/dags/spark.py', dag=dag)
visualization = BashOperator(task_id='run_visualization', bash_command='streamlit run /opt/airflow/dags/visualization2.py', dag=dag)
spark >> visualization
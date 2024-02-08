from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import datetime
from datetime import timedelta

dag1 = DAG(
    dag_id='dag1',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2024, 1, 1),
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 0,
    },
    schedule_interval='@yearly',  # Change this to '@once' if you want to run once
    catchup=False,
)

fetch_raw_data_task = BashOperator(
    task_id='fetch_raw_data',
    bash_command='python3 /home/hadoop/Bureau/ECBD/scripts/fetch_raw_data.py',
    dag=dag1,
)

trigger_dag2 = TriggerDagRunOperator(
    task_id='trigger_dag2',
    trigger_dag_id='dag2',
    dag=dag1,
)

fetch_raw_data_task >> trigger_dag2

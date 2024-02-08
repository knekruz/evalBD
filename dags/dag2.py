from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import datetime
from datetime import timedelta

dag2 = DAG(
    dag_id='dag2',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2024, 1, 1),
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 0,
    },
    schedule_interval=None,
    catchup=False,
)

filter_raw_category_task = BashOperator(
    task_id='filter_raw_category',
    bash_command='python3 /home/hadoop/Bureau/ECBD/spark/filter_raw_category.py',
    dag=dag2,
)

trigger_dag3 = TriggerDagRunOperator(
    task_id='trigger_dag3',
    trigger_dag_id='dag3',
    dag=dag2,
)

filter_raw_category_task >> trigger_dag3

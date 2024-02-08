from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import datetime
from datetime import timedelta

dag3 = DAG(
    dag_id='dag3',
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

enrich_category_task = BashOperator(
    task_id='enrich_category',
    bash_command='python3 /home/hadoop/Bureau/ECBD/spark/enrich_category.py',
    dag=dag3,
)

enrich_category_task

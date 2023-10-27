from airflow import DAG
from datetime import datetime
from scrapy_salarios_engdados import getdata
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator


default_args = {
    "owner": "teste",
    "start_date": datetime(2023, 10, 14),
}

dag = DAG(
    "eng_dados_extraction",
    default_args=default_args,
    schedule_interval="0 6 * * 1-5",
    max_active_runs=1,
)

start_pipeline = DummyOperator(
    task_id="start_pipeline",
    dag=dag
)

extract_glassdoor = PythonOperator(
    task_id='extract_glassdoor',
    python_callable=getdata,
    dag=dag
)

done_pipeline = DummyOperator(
    task_id="done_pipeline",
    dag=dag
)

start_pipeline >> extract_glassdoor >> done_pipeline
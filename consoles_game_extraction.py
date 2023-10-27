from airflow import DAG
from datetime import datetime
from scrapy_consoles_games import get_kabum
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator


default_args = {
    "owner": "teste",
    "start_date": datetime(2023, 10, 14),
}

dag = DAG(
    "consoles_game_extraction",
    default_args=default_args,
    schedule_interval="0 6 * * 1-5",
    max_active_runs=1,
)

start_pipeline = DummyOperator(
    task_id="start_pipeline",
    dag=dag
)

extract_kabum = PythonOperator(
    task_id='extract_kabum',
    python_callable=get_kabum,
    dag=dag
)

done_pipeline = DummyOperator(
    task_id="done_pipeline",
    dag=dag
)

start_pipeline >> extract_kabum >> done_pipeline
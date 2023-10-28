from airflow import DAG
from datetime import datetime
from fifa import nacao,liga,clube,jogadores
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

extract_nacao = PythonOperator(
    task_id='extract_nacao',
    python_callable= nacao,
    dag=dag
)

extract_liga = PythonOperator(
    task_id='extract_liga',
    python_callable=liga,
    dag=dag
)

extract_clube = PythonOperator(
    task_id='extract_clube',
    python_callable=clube,
    dag=dag
)

extract_jogadores = PythonOperator(
    task_id='extract_jogadores',
    python_callable=jogadores,
    dag=dag
)

done_pipeline = DummyOperator(
    task_id="done_pipeline",
    dag=dag
)

start_pipeline >> extract_nacao >> extract_liga >> extract_clube >> extract_jogadores >> done_pipeline
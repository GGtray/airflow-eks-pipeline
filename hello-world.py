from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'me',
    'start_date': datetime(2019, 6, 27, 0, 0, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}


def some_condition():
    a = 1
    if a > 2:
        return 'second_pipeline'
    return 'first_pipeline'


dag = DAG(dag_id='branching',
          default_args=default_args,
          max_active_runs=4,
          schedule_interval='0 * * * *',
          catchup=False)

start_task = DummyOperator(task_id='start_task', dag=dag)

branch = BranchPythonOperator(task_id='validation', python_callable=some_condition, dag=dag)

first_pipeline = DummyOperator(task_id='first_pipeline', dag=dag)

second_pipeline = DummyOperator(task_id='second_pipeline', dag=dag)

first_pipeline_next_step = DummyOperator(task_id='first_pipeline_next_step', dag=dag)
second_pipeline_next_step = DummyOperator(task_id='second_pipeline_next_step', dag=dag)

start_task >> branch
branch >> first_pipeline >> first_pipeline_next_step
branch >> second_pipeline >> second_pipeline_next_step


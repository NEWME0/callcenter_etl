from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def callable_task_01(**context):
    print(context)


def callable_task_02(**context):
    print(context)


with DAG(
    dag_id='external_pbx_workflow',
    schedule_interval='0 0 * * *',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=['example', 'example2'],
    params={"example_key": "example_value"},
) as dag:
    task_01 = PythonOperator(task_id='external_pbx_task_01', python_callable=callable_task_01)
    task_02 = PythonOperator(task_id='external_pbx_task_02', python_callable=callable_task_02)

    task_02 >> task_01


if __name__ == '__main__':
    dag.cli()

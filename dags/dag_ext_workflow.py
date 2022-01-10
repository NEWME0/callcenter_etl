from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator


with DAG(
    dag_id='manually_created_dag',
    schedule_interval='0 0 * * *',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=['example', 'example2'],
    params={"example_key": "example_value"},
) as dag:
    run_this_last = DummyOperator(task_id='run_this_last')

    run_this = BashOperator(task_id='run_after_loop', bash_command='echo 1',)
    run_this >> run_this_last

    for i in range(3):
        task = BashOperator(task_id='runme_' + str(i), bash_command='echo "{{ task_instance_key_str }}" && sleep 1')
        task >> run_this

    also_run_this = BashOperator(task_id='also_run_this', bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',)
    also_run_this >> run_this_last


if __name__ == "__main__":
    dag.cli()
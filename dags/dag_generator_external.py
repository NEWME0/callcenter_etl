from time import sleep
from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.models.baseoperator import chain
from airflow.operators.python import PythonOperator

from plugins.callcenter.apps.external.tasks import ext_scan_recordings


# default dag settings
dag_defaults = {
    'schedule_interval': '0 1 * * *',
    'start_date': datetime(2022, 1, 1),
    'catchup': False,
    'tags': ['external']
}


def ext_process_recordings(*args, **kwargs):
    sleep(3)
    print(args, kwargs)


def ext_download_recordings(*args, **kwargs):
    sleep(3)
    print(args, kwargs)


def ext_convert_recordings(*args, **kwargs):
    sleep(3)
    print(args, kwargs)


def ext_export_recordings(*args, **kwargs):
    sleep(3)
    print(args, kwargs)


def create_dag_external(pbx_id: str, **kwargs):
    # generate dag name
    dag_id = f'external_{pbx_id}'

    # create dag
    dag = DAG(dag_id, default_args=dag_defaults, **kwargs)

    # setup dag tasks
    chain(
        PythonOperator(
            dag=dag,
            task_id=ext_scan_recordings.__name__,
            python_callable=ext_scan_recordings,
            provide_context=True
        ),
        PythonOperator(
            dag=dag,
            task_id=ext_process_recordings.__name__,
            python_callable=ext_process_recordings,
            provide_context=True
        ),
        PythonOperator(
            dag=dag,
            task_id=ext_download_recordings.__name__,
            python_callable=ext_download_recordings,
            provide_context=True
        ),
        PythonOperator(
            dag=dag,
            task_id=ext_convert_recordings.__name__,
            python_callable=ext_convert_recordings,
            provide_context=True
        ),
        PythonOperator(
            dag=dag,
            task_id=ext_export_recordings.__name__,
            python_callable=ext_export_recordings,
            provide_context=True
        )
    )

    return dag


external_pbx = Variable.get('external_pbx', default_var={}, deserialize_json=True)


for pbx_key, dag_settings in external_pbx.items():
    pbx_dag = create_dag_external(pbx_key, **dag_settings)
    globals()[pbx_dag.dag_id] = pbx_dag

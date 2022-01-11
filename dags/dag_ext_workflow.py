from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator


dag_defaults = {
    'schedule_interval': '0 1 * * *',
    'start_date': datetime(2022, 1, 1),
    'catchup': False,
    'tags': ['external']
}


def create_dag_ext_workflow(conn_id: str, **kwargs):
    # generate dag name
    dag_id = f'ext_workflow_{conn_id}'

    # collect dag kwargs
    dag_kwargs = dag_defaults.copy()
    dag_kwargs.update(kwargs)

    # create dag
    dag = DAG(dag_id, **dag_kwargs)

    # setup dag tasks
    chain(
        DummyOperator(dag=dag, task_id='ext_scan_recordings'),
        DummyOperator(dag=dag, task_id='ext_process_recordings'),
        DummyOperator(dag=dag, task_id='ext_download_recordings'),
        DummyOperator(dag=dag, task_id='ext_convert_recordings'),
        DummyOperator(dag=dag, task_id='ext_export_recordings'),
    )

    return dag


ext_connections = Variable.get('ext_connections', default_var={}, deserialize_json=True)


for connection_id, dag_settings in ext_connections.items():
    new_dag = create_dag_ext_workflow(connection_id, **dag_settings)
    globals()[new_dag.dag_id] = new_dag

from datetime import datetime

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.models.variable import Variable
from airflow.operators.dummy import DummyOperator


dag_defaults = dict(
    shedule_interval=None,
    start_date=datetime(2022, 1, 1),
    end_date=None,
    catchup=False,
    tags=['external']
)


def create_dag(conn_id: str, **kwargs) -> DAG:
    # Generate name for dag
    dag_id = f'ext_workflow_{conn_id}'

    # Combine kwargs for dag
    dag_kwargs = dag_defaults.copy()
    dag_kwargs.update(kwargs)

    # Create dag
    dag = DAG(dag_id, **dag_kwargs)

    # Setup dag tasks
    with dag:
        task_scan_recordings = DummyOperator(task_id='task_scan_recordings', dag=dag)
        task_process_recordings = DummyOperator(task_id='task_process_recordings', dag=dag)
        task_download_recordings = DummyOperator(task_id='task_download_recordings', dag=dag)
        task_convert_recordings = DummyOperator(task_id='task_convert_recordings', dag=dag)
        task_export_recordings = DummyOperator(task_id='task_export_recordings', dag=dag)

        chain(
            task_scan_recordings,
            task_process_recordings,
            task_download_recordings,
            task_convert_recordings,
            task_export_recordings
        )

    return dag


# Get settings of connectors to be processed as external from variables
ext_conn_ids = Variable.get('EXT_CONN_IDS', default_var={}, deserialize_json=True)


# Create dag for each connection in EXT_CONN_IDS and append it to globals
for connection_id, connection_dag_kwargs in ext_conn_ids.items():
    connection_dag = create_dag(connection_id, **connection_dag_kwargs)
    globals()[connection_dag.dag_id] = connection_dag

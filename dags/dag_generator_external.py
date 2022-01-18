from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.models.baseoperator import chain

from call_recordings.operators.external import (
    ScanOperator,
    ParseOperator,
    DownloadOperator,
    ConvertOperator,
    ExportOperator
)


# default dag settings
default_args = {
    'schedule_interval': '0 1 * * *',
    'start_date': datetime(2022, 1, 1),
    'catchup': False,
    'tags': ['external']
}


def create_dag_external(key: str, **kwargs):
    # generate dag name
    dag_id = f'external_{key}'

    # setup kwargs
    kwargs.setdefault('max_active_runs', 1)

    # create dag
    dag = DAG(dag_id, default_args=default_args, **kwargs)

    # setup dag tasks
    chain(
        ScanOperator(dag=dag, task_id='external_scan_recordings'),
        ParseOperator(dag=dag, task_id='external_parse_recordings'),
        DownloadOperator(dag=dag, task_id='external_download_recordings'),
        ConvertOperator(dag=dag, task_id='external_convert_recordings'),
        ExportOperator(dag=dag, task_id='external_export_recordings')
    )

    return dag


external_pbx = Variable.get('external_pbx', default_var={}, deserialize_json=True)


for pbx_id, dag_settings in external_pbx.items():
    if not isinstance(dag_settings, dict):
        raise ValueError(f'dag_settings of {pbx_id} should be dict!!!')

    dag_settings.setdefault('params', {})

    if not isinstance(dag_settings['params'], dict):
        raise ValueError(f'params from dag_settings of {pbx_id} should be dict!!!')

    dag_settings['params'].setdefault('pbx_id', pbx_id)

    pbx_dag = create_dag_external(pbx_id, **dag_settings)
    globals()[pbx_dag.dag_id] = pbx_dag

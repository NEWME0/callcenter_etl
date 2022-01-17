from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.models.baseoperator import chain

from plugins.callcenter.external.operators import (
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


def create_dag_external(pbx_id: str, **kwargs):
    # generate dag name
    dag_id = f'external_{pbx_id}'

    # create dag
    dag = DAG(dag_id, default_args=default_args, **kwargs)

    # setup dag tasks
    chain(
        ScanOperator(dag=dag, provide_context=True, task_id='external_scan_recordings'),
        ParseOperator(dag=dag, provide_context=True, task_id='external_parse_recordings'),
        DownloadOperator(dag=dag, provide_context=True, task_id='external_download_recordings'),
        ConvertOperator(dag=dag, provide_context=True, task_id='external_convert_recordings'),
        ExportOperator(dag=dag, provide_context=True, task_id='external_export_recordings')
    )

    return dag


external_pbx = Variable.get('external_pbx', default_var={}, deserialize_json=True)


for pbx_key, dag_settings in external_pbx.items():
    pbx_dag = create_dag_external(pbx_key, **dag_settings)
    globals()[pbx_dag.dag_id] = pbx_dag

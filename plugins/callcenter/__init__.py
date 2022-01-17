from airflow.plugins_manager import AirflowPlugin

from plugins.callcenter.external.operators import (
    ScanOperator,
    ParseOperator,
    DownloadOperator,
    ConvertOperator,
    ExportOperator
)


class CallCenterPlugin(AirflowPlugin):
    name = 'CallCenterPlugin'
    operators = [
        ScanOperator,
        ParseOperator,
        DownloadOperator,
        ConvertOperator,
        ExportOperator
    ]
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []

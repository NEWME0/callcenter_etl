from flask import Blueprint
from airflow.plugins_manager import AirflowPlugin

from call_recordings.operators.external import (
    ScanOperator,
    ParseOperator,
    DownloadOperator,
    ConvertOperator,
    ExportOperator
)


class CallRecordingsPlugin(AirflowPlugin):
    name = 'CallRecordingsPlugin'
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
    appbuilder_views = []

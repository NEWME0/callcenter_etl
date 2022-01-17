from flask import Blueprint
from airflow.plugins_manager import AirflowPlugin

from call_recordings.views.common import ExtensionAgentView, ExtensionGroupView
from call_recordings.operators.external import (
    ScanOperator,
    ParseOperator,
    DownloadOperator,
    ConvertOperator,
    ExportOperator
)


menu_category = 'CallRecordings'


# Creating a flask blueprint to integrate the templates and static folder
call_recordings_blueprint = Blueprint(
    "call_recordings",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/call_recordings",
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
    flask_blueprints = [
        call_recordings_blueprint
    ]
    menu_links = []
    appbuilder_views = [
        {
            "category": menu_category,
            "name": "Extension agents",
            "view": ExtensionAgentView()
        },
        {
            "category": menu_category,
            "name": "Extension groups",
            "view": ExtensionGroupView()
        },
    ]

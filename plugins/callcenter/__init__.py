from airflow.plugins_manager import AirflowPlugin

from callcenter.views.common import ExtensionAgentView, ExtensionGroupView
from callcenter.operators.external import (
    ScanOperator,
    ParseOperator,
    DownloadOperator,
    ConvertOperator,
    ExportOperator
)


menu_category = 'CallRecordings'


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

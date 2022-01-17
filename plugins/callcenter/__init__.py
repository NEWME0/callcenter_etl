from airflow.plugins_manager import AirflowPlugin

from callcenter.common.views import extension_agent_view, extension_group_view
from callcenter.external.operators import (
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
    admin_views = [
        extension_agent_view,
        extension_group_view
    ]
    flask_blueprints = []
    menu_links = []

from flask import current_app
from flask_appbuilder import BaseView, expose
from wtforms import validators
from airflow.www.views import AirflowModelView
from airflow.security import permissions

from call_recordings.models.common import ExtensionAgent, ExtensionGroup


RESOURCE_EXTENSION_AGENT = 'Extension Agents'
RESOURCE_EXTENSION_GROUP = 'Extension Groups'


def _can_create_extension_agent() -> bool:
    return current_app.appbuilder.sm.has_access(permissions.ACTION_CAN_CREATE, RESOURCE_EXTENSION_AGENT)


class ExtensionAgentView(AirflowModelView):
    route_base = '/extension-agent'

    list_template = 'extension_agent_list.html'
    edit_template = 'extension_agent_edit.html'

    datamodel = AirflowModelView.CustomSQLAInterface(ExtensionAgent)

    class_permission_name = RESOURCE_EXTENSION_AGENT
    method_permission_name = {
        'add': 'create',
        'list': 'read',
        'edit': 'edit',
        'delete': 'delete'
    }
    base_permissions = [
        permissions.ACTION_CAN_CREATE,
        permissions.ACTION_CAN_READ,
        permissions.ACTION_CAN_EDIT,
        permissions.ACTION_CAN_DELETE,
        permissions.ACTION_CAN_ACCESS_MENU,
    ]

    list_columns = ['id', 'pbx_id', 'extension', 'fullname']
    add_columns = ['pbx_id', 'extension', 'fullname']
    edit_columns = ['pbx_id', 'extension', 'fullname']
    search_columns = ['id', 'pbx_id', 'extension', 'fullname']

    base_order = ('id', 'asc')

    validators_columns = {
        'pbx_id': [validators.DataRequired()],
        'extension': [validators.DataRequired()],
        'fullname': [validators.DataRequired()],
    }

    extra_args = {
        "can_create_extension_agent": _can_create_extension_agent
    }


def _can_create_extension_group() -> bool:
    return current_app.appbuilder.sm.has_access(permissions.ACTION_CAN_CREATE, RESOURCE_EXTENSION_GROUP)


class ExtensionGroupView(AirflowModelView):
    route_base = '/extension-group'

    list_template = 'extension_group_list.html'
    edit_template = 'extension_group_edit.html'

    datamodel = AirflowModelView.CustomSQLAInterface(ExtensionGroup)

    class_permission_name = RESOURCE_EXTENSION_GROUP
    method_permission_name = {
        'add': 'create',
        'list': 'read',
        'edit': 'edit',
        'delete': 'delete'
    }
    base_permissions = [
        permissions.ACTION_CAN_CREATE,
        permissions.ACTION_CAN_READ,
        permissions.ACTION_CAN_EDIT,
        permissions.ACTION_CAN_DELETE,
        permissions.ACTION_CAN_ACCESS_MENU,
    ]

    list_columns = ['id', 'pbx_id', 'span', 'brand', 'group_of_office', 'office', 'origin', 'group_of_extension']
    add_columns = ['pbx_id', 'span', 'brand', 'group_of_office', 'office', 'origin', 'group_of_extension']
    edit_columns = ['pbx_id', 'span', 'brand', 'group_of_office', 'office', 'origin', 'group_of_extension']
    search_columns = ['pbx_id', 'brand', 'group_of_office', 'office', 'origin', 'group_of_extension']

    base_order = ('id', 'asc')

    validators_columns = {
        'pbx_id': [validators.DataRequired()],
        'span': [validators.DataRequired()],
        'brand': [validators.DataRequired()],
        'group_of_office': [validators.DataRequired()],
        'office': [validators.DataRequired()],
        'origin': [validators.DataRequired()],
        'group_of_extension': [validators.DataRequired()],
    }

    extra_args = {
        "can_create_extension_group": _can_create_extension_group
    }

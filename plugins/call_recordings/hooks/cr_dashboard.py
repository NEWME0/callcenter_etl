from airflow.hooks.base import BaseHook


class CRDashboardHook(BaseHook):
    """
    Custom hook for http api of dashboard (kwg_main_api)
    """

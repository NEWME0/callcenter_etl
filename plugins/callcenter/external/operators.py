from typing import Any

from airflow.models import BaseOperator


class ScanOperator(BaseOperator):
    def execute(self, context: Any):
        print(self.__class__.__name__)
        print(context)


class ParseOperator(BaseOperator):
    def execute(self, context: Any):
        print(self.__class__.__name__)
        print(context)


class DownloadOperator(BaseOperator):
    def execute(self, context: Any):
        print(self.__class__.__name__)
        print(context)


class ConvertOperator(BaseOperator):
    def execute(self, context: Any):
        print(self.__class__.__name__)
        print(context)


class ExportOperator(BaseOperator):
    def execute(self, context: Any):
        print(self.__class__.__name__)
        print(context)

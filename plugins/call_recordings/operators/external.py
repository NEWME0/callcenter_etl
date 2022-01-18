import re
from hashlib import md5
from typing import Any, List
from pathlib import Path
from datetime import datetime

from airflow.hooks.base import BaseHook
from airflow.models import BaseOperator, Variable
from airflow.providers.ftp.hooks.ftp import FTPHook

from call_recordings.utils.functional import partition
from call_recordings.models.external import Base, Recording


class RecordingScan(BaseOperator):
    def execute(self, context: Any):
        ...


class ScanOperator(BaseOperator):
    def execute(self, context: Any):
        # get params from context
        params = context.get('params', {})
        pbx_id = params.get('pbx_id')

        # get root_path from connector params or use current directory
        root_path = params.get('root_path', '.')
        root_path_object = Path(root_path)
        assert not root_path_object.is_absolute(), "root_path param shouldn't be an absolute path!" \
                                                   "Remove '/' (slash) at start of 'root_path'."

        # generate date folders from datetime using given format or use default (2022/01/10)
        scan_date: datetime = context.get('data_interval_start')
        date_path_format = params.get('date_path_format', '%Y/%m/%d')
        date_path = scan_date.strftime(date_path_format)
        date_path_object = Path(date_path)
        assert not date_path_object.is_absolute(), "date_path_format shouldn't generate an absolute path!" \
                                                   "Remove '/' (slash) at start of 'date_path_format'."

        # join root_path and date_path
        scan_path_object = root_path_object.joinpath(date_path_object)
        scan_path = scan_path_object.as_posix()
        print(f'Scan path: {scan_path}')

        # get source connection
        conn_id = params.get('conn_id')

        # execute listdir for current date
        with BaseHook.get_hook(conn_id) as source_hook:
            source_hook: FTPHook = source_hook
            directory_items: List[str] = source_hook.list_directory(scan_path)

        print(f"Scanned objects: {len(directory_items)}")

        # define pattern to match audio and not audio by filenames
        is_audio = re.compile(r'^.*\.(?:wav|mp3)$')

        # filter only audio formats
        other_items, audio_items = partition(values=directory_items, predicate=lambda item: bool(is_audio.match(item)))
        print(f"Not audio: {len(other_items)}. Audio: {audio_items}")

        # save validated file paths
        target_conn_id = Variable.get('target_conn_id')
        target_conn = BaseHook.get_hook(target_conn_id)
        target_engine = target_conn.get_sqlalchemy_engine()

        # ensure base is has needed tables
        Base.prepare(target_engine)

        # prepare values for insertion
        recording_values = [
            {
                'hash': md5(source_path.encode()).hexdigest(),
                'pbx_id': pbx_id,
                'scan_date': scan_date.date(),
                'source_path': scan_path_object.joinpath(source_path).as_posix()
            } for source_path in audio_items
        ]

        # create partition if doesn't exists
        Recording.create_partition(pbx_id=pbx_id)

        # bulk insert values
        created_hashes = Recording.bulk_create(target_engine, values=recording_values)
        print(f"Newly created recordings: {created_hashes}")


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

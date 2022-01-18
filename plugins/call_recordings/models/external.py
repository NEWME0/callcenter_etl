from enum import Enum
from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.sql.schema import Column, CheckConstraint, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import Text, Date, DateTime, String
from sqlalchemy.ext.declarative import DeferredReflection

from call_recordings.models.base import Base


class State(str, Enum):
    to_parse = 'to_parse'
    to_download = 'to_download'
    to_convert = 'to_convert'
    to_export = 'to_export'

    failed_at_process = 'failed_at_process'
    failed_at_download = 'failed_at_download'
    failed_at_convert = 'failed_at_convert'
    failed_at_export = 'failed_at_export'

    exported = 'exported'
    ignored = 'ignored'

    @classmethod
    def values(cls) -> List[str]:
        return tuple([element.value for element in cls])  # noqa


class Recording(DeferredReflection, Base):
    # base columns
    hash = Column(String(length=32), nullable=False)
    pbx_id = Column(String(length=250), nullable=False)
    scan_date = Column(Date, nullable=False)
    source_path = Column(Text, nullable=False)

    # parse columns
    call_date = Column(DateTime, nullable=True)
    unique_id = Column(String(length=40), nullable=True)

    # download/convert
    target_path = Column(Text, nullable=True)

    # finite state machine
    state = Column(String(length=40), nullable=False, default=State.to_parse.value)
    comment = Column(Text, nullable=True)

    __tablename__ = 'external_recording'
    __table_args__ = (
        PrimaryKeyConstraint(pbx_id, hash),
        CheckConstraint(f'state in {State.values()}'),
        {
            "postgresql_partition_by": "LIST (pbx_id)"
        }
    )

    @classmethod
    def create_partition(cls, engine: Engine, pbx_id: str):
        partition_name = f'{cls.__tablename__}_{pbx_id}'

        # create if not exists partition of base table for concrete pbx_id
        engine.execute(
            f"CREATE TABLE IF NOT EXISTS {partition_name} "
            f"PARTITION OF {cls.__tablename__} FOR VALUES IN ('{pbx_id}');"
        )

        # create index on partitioned table
        engine.execute(
            f"CREATE INDEX IF NOT EXISTS {partition_name}_scan_date_status_idx "
            f"ON {partition_name}(scan_date, state);"
        )

    @classmethod
    def bulk_create(cls, engine: Engine, values: list):
        statement = insert(cls).values(values).on_conflict_do_nothing().returning(cls.hash)
        return engine.execute(statement=statement).fetchall()

from sqlalchemy import Column, String, Integer

from call_recordings.models.base import Base


class ExtensionGroup(Base):
    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    pbx_id = Column(String(length=250))
    span = Column(String())
    brand = Column(String())
    group_of_office = Column(String())
    office = Column(String())
    origin = Column(String())
    group_of_extension = Column(String())

    # meta
    __tablename__ = 'extension_group'


class ExtensionAgent(Base):
    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    pbx_id = Column(String(length=250))
    fullname = Column(String(length=80))
    extension = Column(String(length=20))

    # meta
    __tablename__ = 'extension_agent'

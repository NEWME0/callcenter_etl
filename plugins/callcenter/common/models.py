from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ExtensionGroup(Base):
    __tablename__ = 'extension_group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pbx_id = Column(String(length=250))
    span = Column(String())
    brand = Column(String())
    group_of_office = Column(String())
    office = Column(String())
    origin = Column(String())
    group_of_extension = Column(String())


class ExtensionAgent(Base):
    __tablename__ = 'extension_agent'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pbx_id = Column(String(length=250))
    fullname = Column(String(length=80))
    extension = Column(String(length=20))

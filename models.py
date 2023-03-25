from sqlalchemy.orm import declarative_base
from sqlalchemy import Table, Column, Integer, String,Boolean,UniqueConstraint,Float

Base = declarative_base()

class repoTable(Base):
    __tablename__ = 'repo'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    title=Column(String(255))
    repolink = Column(String(255))
    status = Column(Boolean)

class UserTable(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    balance = Column(Integer)
    
    
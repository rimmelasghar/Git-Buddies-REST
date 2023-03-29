import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Table, Column, Integer, String,Boolean,UniqueConstraint,Time,ForeignKeyConstraint, Enum
import enum
# from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class loginTable(Base):
    __tablename__ = 'login'

    id = Column(Integer, primary_key=True)
    username = Column(String(50),unique=True)
    full_name = Column(String(50))
    email = Column(String(50))
    password = Column(String(255))
    disabled = Column(Boolean, default=False)

    __table_args__ = (UniqueConstraint('username'),)


class repoTable(Base):
    __tablename__ = 'repo'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    repolink = Column(String(255))
    status = Column(Boolean)
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['login.id']),
    )  

class UserTable(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    balance = Column(Integer)
    
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['login.id']),
    )  
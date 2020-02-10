from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
    """"""
    __tablename__ = "Users"
 
    id = Column(Integer, primary_key=True, nullable=False, )
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
 
    #----------------------------------------------------------------------
    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password
 


########################################################################
class Message(Base):
    """"""
    __tablename__ = "Messsages"

    id = Column(Integer, primary_key=True, nullable=False)
    id_group = Column(Integer, nullable=False)
    id_user = Column(Integer, nullable=False)
    text = Column(String, nullable=False)

    # ----------------------------------------------------------------------
    def __init__(self, id_group, id_user, text):
        """"""
        self.id_group = id_group
        self.id_user = id_user
        self.text = text


########################################################################
class Group(Base):
    """"""
    __tablename__ = "Groups"

    id = Column(Integer, primary_key=True, nullable=False)
    id_user = Column(Integer, primary_key=True, nullable=False)

    # ----------------------------------------------------------------------
    def __init__(self, id, id_user):
        """"""
        self.id = id
        self.id_user = id_user



# create tables
Base.metadata.create_all(engine)

#-*- coding: utf_8 -*-

from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import desc, asc

Base = declarative_base()


class car(Base):
    __tablename__ = "carousel"
    pic_name = Column(String())
    h1_str = Column(String())
    link = Column(String())
    id = Column(Integer(), primary_key=True)


class higa(Base):
    __tablename__ = "higawari"
    datatime = Column(String())
    id = Column(Integer(), primary_key=True)
    a   = Column(String()))
    b   = Column(String()))
    c   = Column(String()))
    d   = Column(String()))
    e   = Column(String()))
    f   = Column(String()))
    d1  = Column(String()))
    d2  = Column(String()))
    d3  = Column(String()))
    e1  = Column(String()))
    e2  = Column(String()))
    e3  = Column(String()))

    pa  = Column(String()))
    pb  = Column(String()))
    pc  = Column(String()))
    pd  = Column(String()))
    pe  = Column(String()))
    pf  = Column(String()))
    #pd = 1 string not nul)
    #pd = 2 string not nul)
    #pd = 3 string not nul)
    pe1 =  Column(String())
    pe2 =  Column(String())
    pe3 =  Column(String())


class osi(Base):
    __tablename__ = "osirase"
    datatime = Column(String())
    id = Column(Integer(), primary_key=True)
    title = Column(String())


class opi(Base):
    id = Column(Integer(), primary_key=True)
    question = Column(String())
    answer = Column(String())
    datatime = Column(String())

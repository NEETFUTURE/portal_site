#-*- coding: utf_8 -*-

from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import desc, asc

Base = declarative_base()

#Columnにnullable = Falseって引数与えるとnot nullになるらしいです

class Carousel(Base):
    __tablename__ = "carousel"
    pic_name = Column(String())
    h1_str = Column(String())
    link = Column(String())
    id = Column(Integer(), primary_key=True)


class Higawari(Base):
    __tablename__ = "higawari"
    time = Column(String())
    id = Column(Integer(), primary_key=True)
    a   = Column(String())
    b   = Column(String())
    c   = Column(String())
    d   = Column(String())
    e   = Column(String())
    f   = Column(String())
    d1  = Column(String())
    d2  = Column(String())
    d3  = Column(String())
    e1  = Column(String())
    e2  = Column(String())
    e3  = Column(String())

    pa  = Column(String())
    pb  = Column(String())
    pc  = Column(String())
    pd  = Column(String())
    pe  = Column(String())
    pf  = Column(String())
    #pd = 1 string not nu))
    #pd = 2 string not nu))
    #pd = 3 string not nu))
    pe1 =  Column(String())
    pe2 =  Column(String())
    pe3 =  Column(String())


class Osirase(Base):
    __tablename__ = "osirase"
    time = Column(String())
    id = Column(Integer(), primary_key=True)
    title = Column(String())


class Opinion(Base):
    __tablename__ = "opinion"
    id = Column(Integer(), primary_key=True)
    question = Column(String())
    answer = Column(String())
    time = Column(String())


#おまじない x 4

Session = sessionmaker(\
    bind=create_engine("sqlite:///carousel.db", echo=True)\
    )
car_session = Session()

Session = sessionmaker(\
    bind=create_engine("sqlite:///osirase.db", echo=True)\
    )
osi_session = Session()

Session = sessionmaker(\
    bind=create_engine("sqlite:///higawari.db", echo=True)\
    )
hig_session = Session()

Session = sessionmaker(\
    bind=create_engine("sqlite:///opinion.db", echo=True)\
    )
opi_session = Session()

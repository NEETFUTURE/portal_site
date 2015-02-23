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
    __Session__ = sessionmaker(\
    bind=create_engine("sqlite:///carousel.db", echo=True)\
    )
    pic_name = Column(String())
    h1_str = Column(String())
    link = Column(String())
    id = Column(Integer(), primary_key=True)

    session = __Session__()

    @classmethod
    def get_dict(cls):
        l=[]
        for i in cls.session.query(cls).all():
            l.append({"id":i.id,"link":i.link,"h1_str":i.h1_str})
        return l



class Higawari(Base):
    __tablename__ = "higawari"
    __Session__ = sessionmaker(\
    bind=create_engine("sqlite:///higawari.db", echo=True)\
    )
    id = Column(Integer(), primary_key=True)
    time = Column(String(), nullable=False)
    a   = Column(String(), nullable=False)
    b   = Column(String(), nullable=False)
    c   = Column(String(), nullable=False)
    d   = Column(String(), nullable=False)
    e   = Column(String(), nullable=False)
    f   = Column(String(), nullable=False)
    d1  = Column(String(), nullable=False)
    d2  = Column(String(), nullable=False)
    d3  = Column(String(), nullable=False)
    e1  = Column(String())
    e2  = Column(String())
    e3  = Column(String())

    vote_a  = Column(Integer(), default=0)
    vote_b  = Column(Integer(), default=0)
    vote_c  = Column(Integer(), default=0)
    vote_d  = Column(Integer(), default=0)
    vote_e  = Column(Integer(), default=0)
    vote_f  = Column(Integer(), default=0)
    vote_d1 = Column(Integer(), default=0)
    vote_d2 = Column(Integer(), default=0)
    vote_d3 = Column(Integer(), default=0)
    vote_e1 =  Column(Integer(), default=0)
    vote_e2 =  Column(Integer(), default=0)
    vote_e3 =  Column(Integer(), default=0)

    session = __Session__()

    @classmethod
    def return1st_by_id(cls,id):
        return cls.session.query(cls).filter_by(id=id).first()


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
    bind=create_engine("sqlite:///osirase.db", echo=True)\
    )
osi_session = Session()


Session = sessionmaker(\
    bind=create_engine("sqlite:///opinion.db", echo=True)\
    )
opi_session = Session()



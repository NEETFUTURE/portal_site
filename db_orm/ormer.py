#-*- coding: utf_8 -*-

from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import desc, asc
import datetime


def changeStringToDatetime(str_data):
    """
    strのフォーマットはyear/month/day/hour/minute/second
    """
    a = str_data.split("/")
    a = list(map(int,a))
    return datetime.datetime(*a)


def changeDatetimeToString(date,num):
    y = date.year
    m = date.month
    d = date.day
    h = date.hour
    mi = date.minute
    s = date.second

    if num == 3:
        return "%s/%s/%s"%(y,m,d)
    else:
        return "%s/%s/%s/%s/%s/%s"%(y,m,d,h,mi,s)


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

    #Carouselテーブルの内容をすべて辞書にまとめて返す
    @classmethod
    def get_dict(cls):
        l=[]
        for i in cls.session.query(cls).all():
            l.append({"id":i.id,"link":i.link,"h1_str":i.h1_str})
        return l

    #IDで指定したレコードを削除
    @classmethod
    def delById(cls,id):
        target=cls.session.query(cls).filter_by(id=id).first()
        cls.session.delete(target)
        cls.session.commit()

    #IDで指定したカラムの文字列とリンクを更新
    @classmethod
    def updateLink(cls,id,h1_str,link):
        target=cls.session.query(cls).filter_by(id=id).first()
        target.h1_str=h1_str
        target.link=link
        cls.session.commit()




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
    __Session__ = sessionmaker(\
    bind=create_engine("sqlite:///osirase.db", echo=True)\
    )
    time = Column(String())
    id = Column(Integer(), primary_key=True)
    title = Column(String())
    link = Column(String())

    session = __Session__()

    @classmethod
    def delData(cls,id):
        target=cls.session.query(cls).filter_by(id=id).first()
        cls.session.delete(target)
        cls.session.commit()

    @classmethod
    def getData(cls,id):
        return cls.session.query(cls).filter_by(id=id).first()

    @classmethod
    def getAllData(cls):
        return cls.session.query(cls).all()

    @classmethod
    def setData(cls,title,link):
        target=cls.session.query(cls).filter_by(id=id).first()
        target.time=datetime.date.today().strftime("%Y/%m/%d")
        target.title=title
        target.link=link
        cls.session.commit()

    @classmethod
    def addData(cls,title,link):
        ob=Osirase(title=title,
                   link=link,
                   time=datetime.date.today().strftime("%Y/%m/%d"))
        cls.session.add(ob)
        cls.session.commit()

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

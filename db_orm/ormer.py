#-*- coding: utf_8 -*-

from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import desc, asc
import datetime


iden_list_2 = ["a","b","c","d","e","f","r"]
iden_list_m2 = ["pa","udo","soba","ra","rb"]


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




# class Higawari(Base):
#     __tablename__ = "higawari"
#     __Session__ = sessionmaker(\
#     bind=create_engine("sqlite:///higawari.db", echo=True)\
#     )
#     a   = Column(String(), nullable=False)
#     b   = Column(String(), nullable=False)
#     c   = Column(String(), nullable=False)
#     d   = Column(String(), nullable=False)
#     e   = Column(String(), nullable=False)
#     f   = Column(String(), nullable=False)
#     d1  = Column(String(), nullable=False)
#     d2  = Column(String(), nullable=False)
#     d3  = Column(String(), nullable=False)
#     e1  = Column(String())
#     e2  = Column(String())
#     e3  = Column(String())

#     vote_a  = Column(Integer(), default=0)
#     vote_b  = Column(Integer(), default=0)
#     vote_c  = Column(Integer(), default=0)
#     vote_d  = Column(Integer(), default=0)
#     vote_e  = Column(Integer(), default=0)
#     vote_f  = Column(Integer(), default=0)
#     vote_d1 = Column(Integer(), default=0)
#     vote_d2 = Column(Integer(), default=0)
#     vote_d3 = Column(Integer(), default=0)
#     vote_e1 =  Column(Integer(), default=0)
#     vote_e2 =  Column(Integer(), default=0)
#     vote_e3 =  Column(Integer(), default=0)

#     session = __Session__()

#     @classmethod
#     def return1st_by_id(cls,id):
#         return cls.session.query(cls).filter_by(id=id).first()


class Higawari2(Base):
    __tablename__ = "higawari2"
    __Session__ = sessionmaker(\
    bind=create_engine("sqlite:///higawari2.db", echo=True)\
    )
    id = Column(Integer(), primary_key=True)
    time = Column(String())
    name = Column(String())
    identify = Column(String())
    price = Column(Integer())
    vote = Column(Integer(), default=0)

    session = __Session__()

    @classmethod
    def return_desclist_by_date(cls, d_str):
        l = []
        for h in cls.session.query(cls).order_by(desc(cls.vote)).filter_by(time=d_str):
            l.append(dict(name=h.name,
                          identify=h.identify,
                          price=h.price,
                          vote=h.vote))
        return l

    @classmethod
    def return_1st_by_identify(cls, identify):
        return cls.session.query(cls).filter_by(identify=identify).first()


    @classmethod
    def return_by_IdentandDate(cls, identify, str_date):
        return cls.session.query(cls).filter_by(identify=identify,time=str_date).first()


    @classmethod
    def hogehoge(cls, str_date):
        gaku_2 = []
        gaku_m2 = []
        for name in iden_list_2:
            try:
                gaku_2.append(cls.return_by_IdentandDate(name,str_date).name)
            except:
                pass
        for name in iden_list_m2:
            try:
                gaku_m2.append(cls.return_by_IdentandDate(name,str_date).name)
            except:
                pass
        return gaku_2,gaku_m2


class Bussday(Base):
    __tablename__ = "bussday"
    __Session__ = sessionmaker(\
    bind=create_engine("sqlite:///bussday.db", echo=True)\
    )
    id = Column(Integer(), primary_key=True)
    time = Column(String())

    session = __Session__()

    @classmethod
    def hoge(cls, now, num):
        dates = []
        i = cls.session.query(cls).filter_by(time=now).first().id

        for val in range(i, num+1):
            d = cls.session.query(cls).filter_by(id=val).first().time
            dates.append(d)

        return dates



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

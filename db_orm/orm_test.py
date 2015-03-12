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


def changeDatetimeToString(date):
    y = date.year
    m = date.month
    d = date.day
    h = date.hour
    mi = date.minute
    s = date.second
    return "%s/%s/%s/%s/%s/%s"%(y,m,d,h,mi,s)


Base = declarative_base()

#dbファイルに定義されているhogeテーブルを定義するクラス
#テーブルは事前にsqlite3モジュール等で定義しておく
# class Hoge(Base):
#     __tablename__ = "hoge"

#     id = Column(Integer(), primary_key=True)
#     title = Column(String())
#     text = Column(String())
#     time = Column(String())

class Higawari2(Base):
    __tablename__ = "higawari2"
    id = Column(Integer(), primary_key=True)
    time = Column(String())
    name = Column(String())
    identify = Column(String())
    price = Column(Integer())
    vote = Column(Integer(), default=0)

#おまじない
# engine = create_engine("sqlite:///hoge2.db", echo=True)
# Session = sessionmaker(bind=engine)
# session = Session()
engine = create_engine("sqlite:///higawari2.db", echo=True)
session = sessionmaker(bind=engine)()


#hogeテーブルオブジェクト
# hoge1 = Hoge(title="hgoehoge",text="fugafuga")
# hoge2 = Hoge(title="hgoehoge2",text="fugafuga2")
# #追加
# session.add(hoge1)
# session.add(hoge2)
# #コミット
# session.commit()

# higa1 = Higawari2(time="2015/4/1",
#                   name="日替わり定食A",
#                   identify="a",
#                   price=2000)
# higa2 = Higawari2(time="2015/4/1",
#                   name="日替わり定食B",
#                   identify="b",
#                   price=480)
# higa3 = Higawari2(time="2015/4/2",
#                   name="どんぶり1",
#                   identify="d1",
#                   price=350)
# session.add(higa1)
# session.add(higa2)
# session.add(higa3)
# session.commit()


#全件取得
for h in session.query(Higawari2).all():
    print(h.id)
    print(h.name)
    print(h.time)
    print(h.identify)
    print(h.price)
    print(h.vote)


#全件削除
# for hoge in session.query(Hoge).all():
#     session.delete(hoge)
# session.commit()


#編集
# for hoge in session.query(Hoge).all():
#     hoge.title = "hoge"
#     hoge.text = "fuga"
# session.commit()


#idが2のモノで一番最初のモノのidを取得
# print("-------%s-------"%session.query(Hoge).filter_by(id=2).first().time)


#id昇順
for h in session.query(Higawari2).order_by(asc(Higawari2.price)).filter_by(time="2015/4/1"):
    print(h.price)
#id降順
# print(session.query(Hoge).order_by(desc(Hoge.id)))


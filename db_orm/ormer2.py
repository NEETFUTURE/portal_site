#coding:utf-8
from app import db
from sqlalchemy import desc, asc
import datetime

iden_list_2 = ["a","b","c","d","e","f","r"]
iden_list_m2 = ["pa","udo","soba","ra","rb"]

def changeStringToDatetime(str_date):
    """
    strのフォーマットはyear/month/day/hour/minute/second
    """
    a = str_date.split("/")
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


class Carousel(db.Model):
    __tablename__ = "carousel"
    id = db.Column(db.Integer, primary_key=True)
    pic_name = db.Column(db.String())
    h1_str = db.Column(db.String())
    link = db.Column(db.String())

    def __init__(self,pic_name,h1_str,link):
        self.pic_name = pic_name
        self.h1_str = h1_str
        self.link = link

    def __repr__(self):
        return "<Carousel %r>"%self.pic_name

    #Carouselテーブルの内容をすべて辞書にまとめて返す
    @classmethod
    def get_dict(cls):
        l = []
        for i in cls.query.all():
            l.append(dict(id=i.id,link=i.link,h1_str=i.h1_str))

        return l

    #IDで指定したレコードを削除
    @classmethod
    def delById(cls, id):
        target = cls.query.filter_by(id=id).first()
        db.session.delete(target)
        db.session.commit()

    #IDで指定したカラムの文字列とリンクを更新
    @classmethod
    def updateLink(cls, id, h1_str, link):
        target = cls.query.filter_by(id=id).first()
        target.h1_str = h1_str
        target.link = link
        db.session.commit()


class Higawari2(db.Model):
    __tablename__ = "higawari2"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String())
    name = db.Column(db.String())
    identify = db.Column(db.String())
    price = db.Column(db.Integer)
    vote = db.Column(db.Integer, default=0)

    def __init__(self, time, name, identify, price):
        self.time = time
        self.name = name
        self.identify = identify
        self.price = price

    def __repr__(self):
        return "<Higawari2 %r>"%self.name

    @classmethod
    def return_desclist_by_date(cls, d_str):
        l = []
        for h in cls.query.order_by(desc(cls.vote)).filter_by(time=d_str):
            l.append(dict(name=h.name,
                          identify=h.identify,
                          price=h.price,
                          vote=h.vote))

        return l

    @classmethod
    def return_1st_by_identify(cls, identify):
        return cls.query.filter_by(identify=identify).first()

    @classmethod
    def return_by_IdentandDate(cls, identify, str_date):
        return cls.query.filter_by(identify=identify,time=str_date).first()

    @classmethod
    def hogehoge(cls, str_date):
        gaku_2 = []
        gaku_m2 = []

        for name in iden_list_2:
            try:
                gaku_2.append(cls.return_by_IdentandDate(name, str_date).name)
            except:
                pass

        for name in iden_list_m2:
            try:
                gaku_m2.append(cls.return_by_IdentandDate(name, str_date).name)
            except:
                pass

        return gaku_2,gaku_m2


class Bussday(db.Model):
    __tablename__ = "bussday"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String())

    def __init__(self, time):
        self.time = time

    def __repr__(self):
        return "<Bussday %r>"%self.time

    @classmethod
    def hoge(cls, now, num):
        dates = []
        i = cls.query.filter_by(time=now).first().id

        for val in range(i, num+1):
            d = cls.query.filter_by(id=val).first().time
            dates.append(d)

        return dates


class Osirase(db.Model):
    __tablename__ = "osirase"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String())
    title = db.Column(db.String())
    link = db.Column(db.String())

    def __init__(self, title, time, link):
        self.title = title
        self.link = link
        self.time = time

    def __repr__(self):
        return "<Osirase %r>"%self.title

    @classmethod
    def delData(cls, id):
        target = cls.query.filter_by(id=id).first()
        db.session.delet(target)
        db.session.commit()

    @classmethod
    def getData(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def getAllData(cls):
        return cls.query.all()

    @classmethod
    def setData(cls, title, link):
        target = cls.query.filter_by(id=id).first()
        target.time = datetime.date.today().strftime("%Y/%m/%d")
        target.link = link
        db.session.commit()

    @classmethod
    def addData(cls, title, link):
        ob = Osirase(title=title,
                     link=link,
                     time=datetime.date.today().strftime("%Y/%m/%d"))
        db.session.add(ob)
        db.session.commit()


class Opinion(db.Model):
    __tablename__ = "opinion"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String())
    answer = db.Column(db.String())
    time = db.Column(db.String())

    def __init__(self, question, answer, time):
        self.question = question
        self.answer = answer
        self.time = time

    def __repr__(self):
        return "<Opinion %r>"%self.question

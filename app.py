# -*- coding: utf_8 -*-

from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for
from flask import abort, render_template, flash, send_from_directory, Response
import json
from werkzeug import secure_filename
import os
from datetime import datetime as dtime
import traceback
import sys

from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import desc, asc


Base = declarative_base()

class Higawari(Base):
    __tablename__ = "higawari"
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


CAROUSEL = 'carousel.db'
HIGAWARI = 'higawari.db'
OPINION = 'opinion.db'
OSIRASE = 'osirase.db'
UPLOADDIR = "upload_picture"

engine = create_engine("sqlite:///%s"%HIGAWARI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# higawari1 = Higawari(time="2015/2/21",
#                      a="定食a",
#                      b="定食b",
#                      c="定食c",
#                      d="定食d",
#                      e="定食e",
#                      f="定食f",
#                      d1="どんぶり1",
#                      d2="どんぶり2",
#                      d3="どんぶり3",
#                      e1="その他1",
#                      e2="その他2",
#                      e3="その他3")
# session.add(higawari1)
# session.commit()


app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
@app.route("/index")
def top_page():
    return render_template("top.html")


@app.route("/higawari")
def higawari():
    return render_template("index.html")


@app.route("/rank")
def rank():
    h = session.query(Higawari).filter_by(id=1).first()
    time = h.time
    # menu = [h.a,h.b,h.c,h.d,h.e,h.f,
    #         h.d1,h.d2,h.d3,
    #         h.e1,h.e2,h.e3]
    # vote = [h.vote_a,h.vote_b,h.vote_c,
    #         h.vote_d,h.vote_e,h.vote_f,
    #         h.vote_d1,h.vote_d2,h.vote_d3,
    #         h.vote_e1,h.vote_e2,h.vote_e3]
    menu_vote = [[h.a,h.vote_a],[h.b,h.vote_b],[h.c,h.vote_c],
                 [h.d,h.vote_d],[h.e,h.vote_e],[h.f,h.vote_f],
                 [h.d1,h.vote_d1],[h.d2,h.vote_d2],[h.d3,h.vote_d3],
                 [h.e1,h.vote_e1],[h.e2,h.vote_e2],[h.e3,h.vote_e3]]


    return render_template("rank.html",time=time,menu_vote=menu_vote)


@app.route("/connect", methods=["POST"])
def connect():
    get_json = request.json
    #print get_json
    id_num = int(get_json)
    print(id_num)

    return Response(json.dumps("hoge"))

    #id_numで指定のidの人userを持ってくる
    # if session.get("voting") is None:
    #     #userのvoteカラム更新
    #     user.vote += 1
    #     c = user.vote
    #     db.session.add(user)
    #     db.session.commit()
    #     session["voting"] = True
    #     return Response(json.dumps(c))
    # else:
    #     c = user.vote
    #     return Response(json.dumps(c))


@app.route("/opinion")
def opinion():
    return render_template("index.html")


#ファイルへのリンクを返すルーティング
@app.route("/view_upload/<path:filename>")
def view_upload(filename):
    return send_from_directory(UPLOADDIR, filename)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

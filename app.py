# -*- coding: utf_8 -*-

from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for
from flask import abort, render_template, flash, send_from_directory, Response
from flask.ext.mail import Mail
from flask.ext.mail import Message
import json
from werkzeug import secure_filename
import os
from datetime import datetime as dtime
import traceback
import sys
from db_orm import ormer
import urllib.request
import urllib.parse

CAROUSEL = 'carousel.db'
HIGAWARI = 'higawari.db'
OPINION = 'opinion.db'
OSIRASE = 'osirase.db'
UPLOADDIR = "upload_picture"

POR_MAIL = 'gakusyoku@gmail.com'
POR_MAIL_PASS = 'hogehoge'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = POR_MAIL,
    MAIL_PASSWORD = POR_MAIL_PASS,
))
mail = Mail(app)

def sendmail(data):
    msg = Message(data["title"],
                  sender=data["sender"],
                  recipients=data["recipients"])
    msg.body = data["body"]
    mail.send(msg)
    return True


@app.route("/")
@app.route("/index")
def top_page():
    return render_template("top.html",carousel_list=ormer.Carousel.get_dict())


@app.route("/higawari")
def higawari():
    return render_template("index.html")


@app.route("/rank")
def rank():
    h = ormer.Higawari.return1st_by_id(id=1)
    time = h.time
    menu_vote = []
    for m,v in zip(dir(h)[32:45],dir(h)[49:61]):
        menu_vote.append([m,eval("h.%s"%m),eval("h.%s"%v)])

    menu_vote.sort(key=lambda x:x[2])

    return render_template("rank.html",time=time,menu_vote=menu_vote[::-1])


@app.route("/connect", methods=["POST"])
def connect():
    g = request.json
    h = ormer.Higawari.return1st_by_id(id=1)

    #exec使いたくないけどデータベースのカラム上これの方がシンプル。。。
    exec("""h.vote_%s+=1"""%g)
    ormer.Higawari.session.commit()

    #これまたevalも使いたくないんだけど(ry
    return Response(json.dumps(eval("h.vote_%s"%g)))


@app.route("/opinion")
def opinion():
    return render_template("form.html")

#reCAPCHAを使って認証＆メール送信
@app.route("/sendopinion",methods=["POST"])
def sendopinion():
    if(request.form["g-recaptcha-response"]==""):
        return "画像認証を受けてください"

    url="https://www.google.com/recaptcha/api/siteverify"
    keys={"secret":"6LdLpAMTAAAAAFUPa-eYkMNB-GCCmTxJhkwBMFni",
          "response":request.form["g-recaptcha-response"]}
    res=urllib.request.urlopen(url+"?"+urllib.parse.urlencode(keys))
    d_data=json.loads(res.read().decode("utf-8"))
    if(d_data["success"]==False):
        return types(d_data["success"])


    formdata = {"title" :"要望",
                "sender":POR_MAIL,
                "body"  :request.form["body"],
                "recipients":[POR_MAIL]}
    if(sendmail(formdata)==False):
        return "メール送れなかったのん"

    sendmail({"title" :"投稿を受け取りました",
              "sender":"学食ポータル",
              "body":"""
              あなたのメールを承りました。
              近日中にあなたの質問への解答が行きます。
              もし解答が中々来ない場合でも、他の解答の状態によって変わりますのでお待ちください。
              東京電機大学学生食堂ポータルサイト計画実行委員会""",
              "recipients":[request.form["adress"]]})
    return "送信成功"


#ファイルへのリンクを返すルーティング
@app.route("/view_upload/<path:filename>")
def view_upload(filename):
    return send_from_directory(UPLOADDIR, filename)



if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)

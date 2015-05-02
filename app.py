# -*- coding: utf_8 -*-

from __future__ import with_statement
#from contextlib import closing
#import sqlite3
#from werkzeug import secure_filename
#from datetime import datetime as dtime
#import traceback
#from db_orm import ormer
from flask import Flask, request, session, g, redirect, url_for
from flask import abort, render_template, flash, send_from_directory, Response
from flask.ext.mail import Mail
from flask.ext.mail import Message
import json
import os
import sys
from flask.ext.sqlalchemy import SQLAlchemy
import urllib.request
import urllib.parse

SECRET_KEY = os.urandom(20)
UPLOADDIR = "upload_picture"
USERNAME = "admin@gmail.com"
PASSWORD = "yuruyuriISgod"

POR_MAIL = 'gakusyoku@gmail.com'
POR_MAIL_PASS = 'hogehoge'

basedir = os.path.abspath(os.path.dirname(__file__))

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

app.config["SQLALCHEMY_DATABASE_URI"] =\
 "sqlite:///" + os.path.join(basedir,"data.sqlite")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

mail = Mail(app) #flask-mail
db = SQLAlchemy(app) #flask-sqlalchemy


#2回目以降のimportを防ぐ
if not "ormer" in sys.modules.keys():
    from db_orm.ormer2 import *
else:
    pass

def sendmail(data):
    msg = Message(data["title"],
                  sender=data["sender"],
                  recipients=data["recipients"])
    msg.body = data["body"]
    mail.send(msg)
    return True


dates = []
prev = False
today = ""
iden_list = ["default","a","b","c","d","e","f","r",
             "pa","udo","soba","ra","rb"]


# @app.before_request
# def before_request():
#     h = Higawari.return1st_by_id(id=1)
#     data = h.time
#     data = changeStringToDatetime(data)
#     now = dtime.now()
#     if (now-data).days >= 1:
#         h.time = changeDatetimeToString(now,3)
#         db.session.commit()


@app.route("/")
@app.route("/index")
def top_page():
    return render_template("top.html",
                           carousel_list=Carousel.get_dict(),
                           osirase_list=Osirase.getAllData())


@app.route("/higawari")
def higawari():
    return render_template("index.html")


@app.route("/rank")
def rank():
    today = "2015/5/2" #テスト用の日付
    menu = Higawari2.return_desclist_by_date(today)

    return render_template("rank.html",
                           time=today.replace("/","_"), 
                           menu=menu)


@app.route("/connect", methods=["POST"])
def connect():
    js = request.json.split("*")
    h = Higawari2.return_by_IdentandDate(js[0],js[1].replace("_","/"))
    h.vote += 1
    db.session.commit()

    return Response(json.dumps(h.vote))


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


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if request.method == "POST":
        if username==USERNAME and password==PASSWORD:
            session["login"] = True
            return redirect(url_for("adminpage"))

    return redirect(url_for("top_page"))


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("login", None)
    return redirect(url_for("top_page"))


@app.route("/admin", methods=["POST", "GET"])
def adminpage():
    global dates
    global today
    global prev

    try:
        if not session["login"]:
            return redirect(url_for("top_page"))
    except:
        return redirect(url_for("top_page"))

    car = Carousel.get_dict()

    if "date" in request.form:
        today = request.form["date"]
    elif prev:
        prev = False
        pass
    else:
        #today = ormer.changeDatetimeToString(dtime.now(),3)
        today = "2015/5/2" #テスト用の日付
        dates = Bussday.hoge(today, 4)

    menu = Higawari2.return_desclist_by_date(today)

    files = os.listdir('static/img/')

    return render_template("admin.html",
                           today=today,
                           carousel=car,
                           files=files,
                           osirase=Osirase.getAllData(),
                           ufiles=os.listdir(UPLOADDIR),
                           dates=dates,
                           menu=menu,
                           i_list=iden_list)


@app.route("/change",methods=["POST"])
def change_higawari():
    global today
    global prev
    del_list = []

    try:
        if not session["login"]:
            return redirect(url_for("top_page"))
    except:
        return redirect(url_for("top_page"))

    if request.method == "POST":

        del_list = request.form.getlist("ch")
        for iden in del_list:
            h = Higawari2.return_by_IdentandDate(iden, request.form["today"])
            db.session.delete(h)
        db.session.commit()

        for i in range(0, 10):
            if request.form["s_"+str(i)] == "default" or request.form["s_"+str(i)] in del_list:
                pass
            else:
                ide = request.form["s_"+str(i)]
                d = request.form["today"]
                name = request.form["m_"+str(i)]
                try:
                    price = int(request.form["p_"+str(i)])
                    vote = int(request.form["v_"+str(i)])
                except:
                    price = vote = 0
                h = Higawari2.return_by_IdentandDate(ide, d)
                if h:
                    h.name = name
                    h.price = price
                    h.vote = vote
                    db.session.commit()
                else:
                    h = Higawari2(identify=ide,time=d,name=name,price=price)
                    db.session.add(h)
                    db.session.commit()
        today = request.form["today"]
        prev = True

        return redirect(url_for("adminpage"))

    return redirect(url_for("adminpage"))


@app.route("/change_carousel",methods=["POST"])
def change_carousel():
    if not session["login"]:
        return redirect(url_for("top_page"))

    if(request.method != "POST"):
        return redirect(url_for("adminpage"))

    #データベース更新
    i=1
    while "link_{0}".format(i) in request.form:
        Carousel.updateLink(i,
                            request.form["h1_str_{0}".format(i)],
                            request.form["link_{0}".format(i)])
        i+=1

    return redirect(url_for("adminpage"))


@app.route("/del_osirase",methods=["POST"])
def del_osirase():
    Osirase.delData(request.form['del'])
    return redirect(url_for("adminpage"))


@app.route("/add_osirase",methods=["POST"])
def add_osirase():
    Osirase.addData(request.form['osi_title'],request.form['osi_link'])
    return redirect(url_for("adminpage"))


@app.route("/upload", methods=["POST"])
def upload():
    if not session["login"]:
        return redirect(url_for("top_page"))
    upload_file = request.files.getlist("file[]")

    for f in upload_file:
        f.save(os.path.join(UPLOADDIR,f.filename))

    return redirect(url_for("adminpage"))


#ファイルへのリンクを返すルーティング
@app.route("/view_upload/<path:filename>")
def view_upload(filename):
    return send_from_directory(UPLOADDIR, filename)



if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)

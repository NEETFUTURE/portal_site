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
SECRET_KEY = os.urandom(20)


USERNAME = "admin@gmail.com"
PASSWORD = "yuruyuriISgod"

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



@app.before_request
def before_request():
    h = ormer.Higawari.return1st_by_id(id=1)
    data = h.time
    data = ormer.changeStringToDatetime(data)
    now = dtime.now()
    if (now-data).days >= 1:
        h.time = ormer.changeDatetimeToString(now,3)
        ormer.Higawari.session.commit()


@app.route("/")
@app.route("/index")
def top_page():
    return render_template("top.html",
                           carousel_list=ormer.Carousel.get_dict(),
                           osirase_list=ormer.Osirase.getAllData())


@app.route("/higawari")
def higawari():
    return render_template("index.html")


@app.route("/rank")
def rank():
    h = ormer.Higawari.return1st_by_id(id=1)
    time = h.time
    time = time.replace("/","_")
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



@app.route("/admin")
def adminpage():
    if not session["login"]:
        return redirect(url_for("top_page"))
    car = ormer.Carousel.get_dict()
    hig = ormer.Higawari.return1st_by_id(id=1)
    time = hig.time
    menu_vote = []
    for m,v in zip(dir(hig)[32:45],dir(hig)[49:61]):
        menu_vote.append([m,eval("hig.%s"%m),eval("hig.%s"%v)])
    menu_vote.sort(key=lambda x:x[2])

    files = os.listdir('static/img/')

    return render_template("admin.html",
                           carousel=car,
                           time=time,
                           higawari=menu_vote,
                           files=files,
                           osirase=ormer.Osirase.getAllData(),
                           ufiles=os.listdir(UPLOADDIR))


@app.route("/change",methods=["POST"])
def change_higawari():
    if not session["login"]:
        return redirect(url_for("top_page"))

    col = ["a","b","c","d","e","f","d1","d2","d3","e1","e2","e3"]
    h = ormer.Higawari.return1st_by_id(id=1)

    if request.method == "POST":
        if request.form["day"]:
            h.time = request.form["day"]
        for c in col:
            if request.form[c]:
                exec("""h.%s='%s'"""%(c,request.form[c]))
                exec("""h.vote_%s=0"""%c)
            else:
                pass
        ormer.Higawari.session.commit()

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
        ormer.Carousel.updateLink(i,
                                  request.form["h1_str_{0}".format(i)],
                                  request.form["link_{0}".format(i)])
        i+=1

    return redirect(url_for("adminpage"))

@app.route("/del_osirase",methods=["POST"])
def del_osirase():
    ormer.Osirase.delData(request.form['del'])
    return redirect(url_for("adminpage"))

@app.route("/add_osirase",methods=["POST"])
def add_osirase():
    ormer.Osirase.addData(request.form['osi_title'],request.form['osi_link'])
    return redirect(url_for("adminpage"))

@app.route("/upload", methods=["POST"])
def upload():
    if not session["login"]:
        return redirect(url_for("top_page"))
    upload_file = request.files.getlist("file[]")
    #print("*"*20)
    for f in upload_file:
        #print(f.filename)
        f.save(os.path.join(UPLOADDIR,f.filename))
    #print("*"*20)
    return redirect(url_for("adminpage"))


#ファイルへのリンクを返すルーティング
@app.route("/view_upload/<path:filename>")
def view_upload(filename):
    return send_from_directory(UPLOADDIR, filename)



if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)

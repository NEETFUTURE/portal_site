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


dates = []
prev = False
today = ""
iden_list = ["default","a","b","c","d","e","f","r",
             "pa","udo","soba","ra","rb"]


# @app.before_request
# def before_request():
#     h = ormer.Higawari.return1st_by_id(id=1)
#     data = h.time
#     data = ormer.changeStringToDatetime(data)
#     now = dtime.now()
#     if (now-data).days >= 1:
#         h.time = ormer.changeDatetimeToString(now,3)
#         ormer.Higawari.session.commit()


@app.route("/")
@app.route("/index")
def top_page():
    return render_template("another-top.html",
                           carousel_list=ormer.Carousel.get_dict(),
                           osirase_list=ormer.Osirase.getAllData())


@app.route("/higawari")
def higawari():
    return render_template("index.html")


@app.route("/rank")
def rank():
    # h = ormer.Higawari.return1st_by_id(id=1)
    # time = h.time
    # time = time.replace("/","_")
    # menu_vote = []
    # for m,v in zip(dir(h)[32:45],dir(h)[49:61]):
    #     menu_vote.append([m,eval("h.%s"%m),eval("h.%s"%v)])

    # menu_vote.sort(key=lambda x:x[2])

    # return render_template("rank.html",time=time,menu_vote=menu_vote[::-1])

    #today = ormer.changeDatetimeToString(dtime.now(),3)
    today = "2015/3/23" #テスト用の日付
    menu = ormer.Higawari2.return_desclist_by_date(today)

    return render_template("rank.html",
                           time=today.replace("/","_"), 
                           menu=menu)

@app.route("/connect", methods=["POST"])
def connect():
    # g = request.json
    # h = ormer.Higawari.return1st_by_id(id=1)

    # #exec使いたくないけどデータベースのカラム上これの方がシンプル。。。
    # exec("""h.vote_%s+=1"""%g)
    # ormer.Higawari.session.commit()

    # #これまたevalも使いたくないんだけど(ry
    # return Response(json.dumps(eval("h.vote_%s"%g)))

    js = request.json.split("*")
    h = ormer.Higawari2.return_by_IdentandDate(js[0],js[1].replace("_","/"))
    h.vote += 1
    ormer.Higawari2.session.commit()

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

    car = ormer.Carousel.get_dict()

    if "date" in request.form:
        today = request.form["date"]
    elif prev:
        prev = False
        pass
    else:
        #today = ormer.changeDatetimeToString(dtime.now(),3)
        today = "2015/3/21" #テスト用の日付
        dates = ormer.Bussday.hoge(today, 4)

    menu = ormer.Higawari2.return_desclist_by_date(today)

    files = os.listdir('static/img/')

    return render_template("admin.html",
                           today=today,
                           carousel=car,
                           files=files,
                           osirase=ormer.Osirase.getAllData(),
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
        #print("*"*30)
        #print(del_list)
        for iden in del_list:
            h = ormer.Higawari2.return_by_IdentandDate(iden, request.form["today"])
            ormer.Higawari2.session.delete(h)
        ormer.Higawari2.session.commit()

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
                h = ormer.Higawari2.return_by_IdentandDate(ide, d)
                if h:
                    h.name = name
                    h.price = price
                    h.vote = vote
                    ormer.Higawari2.session.commit()
                else:
                    h = ormer.Higawari2(identify=ide,time=d,name=name,price=price)
                    ormer.Higawari2.session.add(h)
                    ormer.Higawari2.session.commit()
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

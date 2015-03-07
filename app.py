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
from db_orm import ormer

CAROUSEL = 'carousel.db'
HIGAWARI = 'higawari.db'
OPINION = 'opinion.db'
OSIRASE = 'osirase.db'
UPLOADDIR = "upload_picture"



app = Flask(__name__)
app.config.from_object(__name__)


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
    return render_template("index.html")


@app.route("/admin")
def adminpage():
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
                           files=files)


@app.route("/change",methods=["POST"])
def change_higawari():
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
    if(request.method != "POST"):
        return redirect(url_for("adminpage"))
    #ここにデータベース更新機能を書きたい

    return redirect(url_for("adminpage"))


#ファイルへのリンクを返すルーティング
@app.route("/view_upload/<path:filename>")
def view_upload(filename):
    return send_from_directory(UPLOADDIR, filename)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

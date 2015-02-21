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

CAROUSEL = 'carousel.db'
HIGAWARI = 'higawari.db'
OPINION = 'opinion.db'
OSIRASE = 'osirase.db'
UPLOADDIR = "upload_picture"



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
    return render_template("rank.html")


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
    app.run(host="0.0.0.0", debug=True, threaded=True)

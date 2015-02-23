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


UPLOADDIR = "upload_picture"


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
    h = ormer.Higawari.return1st_by_id(id=1)
    time = h.time
    # menu = [h.a,h.b,h.c,h.d,h.e,h.f,
    #         h.d1,h.d2,h.d3,
    #         h.e1,h.e2,h.e3]
    # vote = [h.vote_a,h.vote_b,h.vote_c,
    #         h.vote_d,h.vote_e,h.vote_f,
    #         h.vote_d1,h.vote_d2,h.vote_d3,
    #         h.vote_e1,h.vote_e2,h.vote_e3]
    menu_vote = [["a",h.a,h.vote_a],["b",h.b,h.vote_b],["c",h.c,h.vote_c],
                 ["d",h.d,h.vote_d],["e",h.e,h.vote_e],["f",h.f,h.vote_f],
                 ["d1",h.d1,h.vote_d1],["d2",h.d2,h.vote_d2],["d3",h.d3,h.vote_d3],
                 ["e1",h.e1,h.vote_e1],["e2",h.e2,h.vote_e2],["e3",h.e3,h.vote_e3]]
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

import asyncio
from os import walk
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request
from tparser.aparser import get_data_from_tg
from tparser.db import db
from tparser.models import Channel, Post


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    # scheduler = BackgroundScheduler()
    # scheduler.add_job(get_data_from_tg, "interval", hours=1, id="tg_parser_job")

    @app.route("/")
    def index():
        title = "Telegram parser"
        # jobs = scheduler.get_jobs()
        channels = Channel.query.all()

        return render_template("index.html", page_title=title, channels=channels)

    @app.route("/parse")
    def run_parser():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_data_from_tg())

        return render_template("info.html", job=result)

    @app.route("/channel")
    def channel():
        posts = Post.query.all()

        return render_template("channel.html", posts=posts)

    @app.route("/post/<int:post_id>")
    def get_post(post_id):
        post = Post.query.filter(Post.id == post_id).first()

        return render_template("post.html", post=post)

    return app


# @app.route("/parse")
# def run_parser():
#     job = get_data_from_tg()
#     return render_template("info.html",  job=job)

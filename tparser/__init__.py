from os import walk
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request
from tparser.parser import get_data_from_tg
from tparser.db import db


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
        return render_template("index.html", page_title=title, jobs=[1, 2, 3])
    
    @app.route("/parse")
    def run_parser():
        job = get_data_from_tg()
        return render_template("info.html",  job=job)

    return app

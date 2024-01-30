from flask import Flask, render_template, request
from telegram_parser.db import init_db
from telegram_parser.parser import get_channel_info
def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    init_db(app)

    @app.route('/')
    
    def index():
        title = "Telegram parser"
        return render_template('index.html', page_title=title)
    @app.route('/parser', methods=['GET', 'POST'])  
    def run_parser():
       if request.method == 'GET':
           channel_info = get_channel_info()
           return render_template('info.html', channel_info=channel_info)
                        

    return app



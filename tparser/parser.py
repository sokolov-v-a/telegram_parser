from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from datetime import datetime
from tparser.db import db
from tparser.config import API_ID, API_HASH, CHANNEL_LINK, PHONE_NUMBER, POSTS_LIMIT
from tparser.models import Comment, Post
from tparser.sentiment_analysis import get_sentiment

client = TelegramClient("session_name", API_ID, API_HASH)
client.connect()


def get_data_from_tg():
    entity = client.get_entity(CHANNEL_LINK)
    full_channel = client(GetFullChannelRequest(entity))
    if not client.is_user_authorized():
        client.send_code_request(PHONE_NUMBER)
        client.sign_in(PHONE_NUMBER, input("Enter code: "))

    for message in client.iter_messages(full_channel.full_chat.id, limit=POSTS_LIMIT):
        parse_posts(full_channel, message)
        
        post.get_sentiment_color()
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

    client.disconnect()
    return "Job Done!"


def parse_posts(full_channel, message):
    existing_post = Post.query.filter_by(number=str(message.number)).first()
    if existing_post is None:
        post = Post(
            channel_id=full_channel.id,  # ID канала, 1 по умолчанию
            number=str(message.id),
            text=message.text,
            publication_date=datetime.utcfromtimestamp(message.date.timestamp()),
        )
        db.session.add(post)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        parse_comments(full_channel, post, message)
        post.get_sentiment_color()
        db.session.add(post)  
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()


def parse_comments(full_channel, post, message):
    # Проверка, есть ли у сообщения ответы, прежде чем пытаться их получить
    if message.replies:
        # Попытка получить ответы только при наличии действительного идентификатора сообщения
        reply_message = client.get_messages(full_channel.full_chat.id, ids=message.id)
        for comment in client.iter_messages(full_channel.full_chat.id, reply_to=reply_message.id):
            existing_comment = Post.query.filter_by(number=str(comment.number), post_id=post.id).first()
            if existing_comment is None:
                comment = Comment(
                    post_id=post.id,
                    text=comment.text,
                    number=str(comment.id),
                    sentiment_color=get_sentiment(comment.text),
                )

                db.session.add(comment)
                try:
                    db.session.commit()
                except Exception:
                    db.session.rollback()

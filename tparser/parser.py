from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from datetime import datetime
from tparser.db import db
from tparser.config import API_ID, API_HASH, CHANNEL_LINK, PHONE_NUMBER, POSTS_LIMIT

from tparser.models import Comment, Post

client = TelegramClient("session_name", API_ID, API_HASH)


def get_data_from_tg():
    entity = client.get_entity(CHANNEL_LINK)
    full_channel = client(GetFullChannelRequest(entity))
    if not client.is_user_authorized():
        client.send_code_request(PHONE_NUMBER)
        client.sign_in(PHONE_NUMBER, input("Enter code: "))

    for message in client.iter_messages(full_channel.full_chat.id, limit=POSTS_LIMIT):
        post = Post(
            channel_id=1,  # ID канала, 1 по умолчанию
            number=str(message.id),
            text=message.text,
            publication_date=datetime.utcfromtimestamp(message.date.timestamp()),
        )
        db.session.add(post)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

        # Проверка, есть ли у сообщения ответы, прежде чем пытаться их получить
        if message.replies:
            # Попытка получить ответы только при наличии действительного идентификатора сообщения
            reply_message = client.get_messages(full_channel.full_chat.id, ids=message.id)
            for comment in client.iter_messages(full_channel.full_chat.id, reply_to=reply_message.id):
                comment = Comment(
                    post_id=post.id,
                    text=comment.text,
                    number=str(comment.id),
                    semantic_color=0.0,  # Замените на необходимое значение
                )

                db.session.add(comment)
                try:
                    db.session.commit()
                except Exception:
                    db.session.rollback()

    return 'Job Done!'

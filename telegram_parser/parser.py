from flask import current_app
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import telethon
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from datetime import datetime
from telegram_parser.db import db
from telegram_parser.config import API_ID, API_HASH, CHANNEL_LINK, PHONE_NUMBER, POSTS_LIMIT

from telegram_parser.models import Comment, Post

client = TelegramClient("session_name", API_ID, API_HASH)


async def main():
    await client.connect()
    if not client.is_user_authorized():
        await client.send_code_request(PHONE_NUMBER)


async def get_channel_info():
    entity = await client.get_entity(CHANNEL_LINK)
    full_channel = await client(GetFullChannelRequest(channel=entity))
    return full_channel


# Получение постов и комментариев
async def parse_channel():
    full_channel = await get_channel_info()
    async for message in client.iter_messages(full_channel.full_chat.id, limit=POSTS_LIMIT):
        post = Post(
            channel_id=1,  # ID канала, 1 по умолчанию
            number=str(message.id),
            text=message.text,
            publication_date=datetime.utcfromtimestamp(message.date.timestamp()),
        )
        db.session.add(post)
        db.session.commit()

        # Проверка, есть ли у сообщения ответы, прежде чем пытаться их получить
        if message.replies:
            # Попытка получить ответы только при наличии действительного идентификатора сообщения
            reply_message = await client.get_messages(full_channel.full_chat.id, ids=message.id)
            async for comment in client.iter_messages(full_channel.full_chat.id, reply_to=reply_message.id):
                comment_obj = Comment(
                    post_id=post.id,
                    text=comment.text,
                    number=str(comment.id),
                    semantic_color=0.0,  # Замените на необходимое значение
                )
                db.session.add(comment_obj)
                db.session.commit()


if __name__ == "__main__":
    pass


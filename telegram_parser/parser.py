# telegram_parser.py
# from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
# from .models import Base, Post, Comment
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import telethon
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from flask import current_app
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from datetime import datetime
from .models import Post, Comment

# Создание подключения
#engine = create_engine('sqlite:///telegram_parser.db', echo=True)

# # Создание сессии для взаимодействия с базой данных
# Session = sessionmaker(bind=engine)
# session = Session()

with current_app.app_context():
    # Инициализация Telethon клиента
    client = TelegramClient('session_name', current_app.config['API_ID'], current_app.config['API_HASH'])
    client.connect()
    
    # Авторизация
    if not client.is_user_authorized():
        client.send_code_request(current_app.config['PHONE_NUMBER'])
        client.sign_in(current_app.config['PHONE_NUMBER']), input('Введите код из SMS: ')

    # Получение информации о канале
    async def get_channel_info():
        entity = await client.get_entity(current_app.config['CHANNEL_LINK'])
        full_channel = await client(GetFullChannelRequest(channel=entity))
        return full_channel

    # Получение постов и комментариев
    async def parse_channel():
        full_channel = await get_channel_info()
        async for message in client.iter_messages(full_channel.full_chat.id, limit=current_app.config['POSTS_LIMIT']):
            post = Post(
                channel_id=1,  # ID канала, 1 по умолчанию
                number=str(message.id),
                text=message.text,
                publication_date=datetime.utcfromtimestamp(message.date.timestamp()),
            )
            post.add()
            post.commit()

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
                        comment_obj.add()
                        comment_obj.commit()
 
if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(parse_channel())
  #  session.close()



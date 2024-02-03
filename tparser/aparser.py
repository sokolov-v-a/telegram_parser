import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from datetime import datetime
from tparser.db import db
from tparser.config import API_ID, API_HASH, CHANNEL_LINK, PHONE_NUMBER, POSTS_LIMIT
from tparser.models import Comment, Post
from tparser.sentiment_analysis import get_sentiment


async def get_data_from_tg():
    async with TelegramClient("session_name", API_ID, API_HASH) as client:
        await client.connect()

        entity = await client.get_entity(CHANNEL_LINK)
        full_channel = await client(GetFullChannelRequest(entity))

        if not client.is_user_authorized():
            await client.send_code_request(PHONE_NUMBER)
            await client.sign_in(PHONE_NUMBER, input("Enter code: "))

        async for message in client.iter_messages(full_channel.full_chat.id, limit=POSTS_LIMIT):
            existing_post = Post.query.filter_by(number=str(message.id)).first()
            if existing_post is None:
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
                reply_message = await client.get_messages(full_channel.full_chat.id, ids=message.id)
                async for comment in client.iter_messages(full_channel.full_chat.id, reply_to=reply_message.id):
                    comment_obj = Comment(
                        post_id=comment.id,
                        text=comment.text,
                        number=str(comment.id),
                        sentiment_color=get_sentiment(comment.text),  # Замените на необходимое значение
                    )

                    db.session.add(comment_obj)
                    try:
                        db.session.commit()
                    except Exception:
                        db.session.rollback()

        await client.disconnect()
        return "Job Done!"


if __name__ == "__main__":
    asyncio.run(get_data_from_tg())

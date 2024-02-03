from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)


def get_sentiment(text):
    messages = [text]
    results = model.predict(messages, k=2)
    for message, sentiment in zip(messages, results):
        if "negative" in sentiment:
            # print(message)
            return -round(float(sentiment["negative"]), 2)
        elif "positive" in sentiment:
            # print(message)
            return round(float(sentiment["positive"]), 2)

    return 0.0


# messages = [
#     'Ура! Сегодня хорошая погода',
#     'Я очень рад проводить с тобою время',
#     'Мне нравится эта музыкальная композиция',
#     'В больнице была ужасная очередь',
#     'Этот гад с верхнего этажа мешает спать!',
#     'Маленькая девочка потерялась в торговом центре',
# ]

# results = model.predict(messages, k=2)
# for message, sentiment in zip(messages, results):
#     if 'negative' in sentiment:
#         print(message, ' negative')
#     elif 'positive' in sentiment:
#         print(message, ' positive')
#     else:
#         print(message, '-&gt;', sentiment)

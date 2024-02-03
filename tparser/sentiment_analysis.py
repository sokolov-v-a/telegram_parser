from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

def get_sentiment(text):
    messages = [text]
    results = model.predict(messages, k=2)
    for message, sentiment in zip(messages, results):
        if 'negative' in sentiment:
            return 'negative'
        elif 'positive' in sentiment:
            return 'positive'
    
    return 'neutral'    


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
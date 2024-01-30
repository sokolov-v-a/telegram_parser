# Telegaram parser
Telegaram parser - это приложения для получения статистики по телеграмм каналам
Пользователь вводит ссылку на телеграмм канал и получает статистику по каналу, а именно количество постов, самый популярны пост, симантическую оценку содержания постов.

### Установка

1. Клонируйте репозиторий, создайте виртуальное окружение
2. Установите зависимости `pip install -r requirements.txt`
3. Создайте файл settings.py и создайте в нем переменные:
  ```
  API_ID = '26447359'
  API_HASH = '99fea05ec025c08aa8fd77f1a49c486e'
  PHONE_NUMBER = '+79856191010'
  CHANNEL_LINK = 'https://t.me/rubskyi_official'
  POSTS_LIMIT = 5  # Укажите количество постов, которые вы хотите парсить
  
  API_KEY = "Ключ вашего бота"
  PROXY_URL = "URL socks5-прокси"
  PROXY_USERNAME = "Username для авторизации на прокси"
  PROXY_PASSWORD = "Пароль  для авторизации на прокси"
  USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']
  ```
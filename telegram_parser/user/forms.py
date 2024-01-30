from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    telegram_user_id = StringField('Telegram ID Пользователя ', validators=[DataRequired()])
    email = StringField('Telegram ID Пользователя ', validators=[Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Отправить')

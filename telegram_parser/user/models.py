from datetime import datetime
from telegram_parser import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    telegram_user_id = db.Column(db.String, nullable=False)
    is_activated = db.Column(db.Boolean, default=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    channels = db.relationship('Channel', back_populates='user')

    def delete(self):
        self.is_deleted = True

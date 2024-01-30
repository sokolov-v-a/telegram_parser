from datetime import datetime
from telegram_parser.db import db

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

class Channel(db.Model):
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='channels')
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    link = db.Column(db.String)
    is_deleted = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', back_populates='channel')

    def delete(self):
        self.is_deleted = True

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    channel = db.relationship('Channel', back_populates='posts')
    number = db.Column(db.String, nullable=False)
    text = db.Column(db.String)
    publication_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    comments = db.relationship('Comment', back_populates='post')
    analysis_data = db.relationship('AnalysisData', back_populates='post', uselist=False)

    def delete(self):
        self.is_deleted = True

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    post = db.relationship('Post', back_populates='comments')
    text = db.Column(db.String)
    number = db.Column(db.Integer)
    semantic_color = db.Column(db.Float)
    is_deleted = db.Column(db.Boolean, default=False)

    def delete(self):
        self.is_deleted = True

class AnalysisData(db.Model):
    __tablename__ = 'analysis_data'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    post = db.relationship('Post', back_populates='analysis_data')
    num_likes = db.Column(db.Integer)
    num_views = db.Column(db.Integer)
    num_comments = db.Column(db.Integer)
    semantic_color = db.Column(db.Float)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    def delete(self):
        self.is_deleted = True



# from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Float
# from sqlalchemy.orm import relationship, declarative_base
# # from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime

# Base = declarative_base()

# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True)
#     telegram_user_id = Column(String, nullable=False)
#     is_activated = Column(Boolean, default=False)
#     registration_date = Column(DateTime, default=datetime.utcnow)
#     email = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#     is_deleted = Column(Boolean, default=False)
#     channels = relationship('Channel', back_populates='user')

#     def delete(self):
#         self.is_deleted = True

# class Channel(Base):
#     __tablename__ = 'channels'

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     user = relationship('User', back_populates='channels')
#     name = Column(String, nullable=False)
#     description = Column(String)
#     link = Column(String)
#     is_deleted = Column(Boolean, default=False)
#     posts = relationship('Post', back_populates='channel')

#     def delete(self):
#         self.is_deleted = True

# class Post(Base):
#     __tablename__ = 'posts'

#     id = Column(Integer, primary_key=True)
#     channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
#     channel = relationship('Channel', back_populates='posts')
#     number = Column(String, nullable=False)
#     text = Column(String)
#     publication_date = Column(DateTime, default=datetime.utcnow)
#     is_deleted = Column(Boolean, default=False)
#     comments = relationship('Comment', back_populates='post')
#     analysis_data = relationship('AnalysisData', back_populates='post', uselist=False)

#     def delete(self):
#         self.is_deleted = True

# class Comment(Base):
#     __tablename__ = 'comments'

#     id = Column(Integer, primary_key=True)
#     post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
#     post = relationship('Post', back_populates='comments')
#     text = Column(String)
#     number = Column(Integer)
#     semantic_color = Column(Float)
#     is_deleted = Column(Boolean, default=False)

#     def delete(self):
#         self.is_deleted = True

# class AnalysisData(Base):
#     __tablename__ = 'analysis_data'

#     id = Column(Integer, primary_key=True)
#     post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
#     post = relationship('Post', back_populates='analysis_data')
#     num_likes = Column(Integer)
#     num_views = Column(Integer)
#     num_comments = Column(Integer)
#     semantic_color = Column(Float)
#     analysis_date = Column(DateTime, default=datetime.utcnow)
#     is_deleted = Column(Boolean, default=False)

#     def delete(self):
#         self.is_deleted = True

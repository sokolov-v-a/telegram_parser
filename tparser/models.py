from datetime import datetime
from tparser.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    telegram_user_id = db.Column(db.String, nullable=False)
    is_activated = db.Column(db.Boolean, default=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    channels = db.relationship("Channel", back_populates="user")

    def delete(self):
        self.is_deleted = True

    def __repr__(self):
        return f"User id={self.id} tg_id={self.telegram_user_id}"


class Channel(db.Model):
    __tablename__ = "channels"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="channels")
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    link = db.Column(db.String)
    is_deleted = db.Column(db.Boolean, default=False)
    posts = db.relationship("Post", back_populates="channel")

    def delete(self):
        self.is_deleted = True

    def __repr__(self):
        return f"Channel id={self.id} name={self.name}"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"), nullable=False)
    channel = db.relationship("Channel", back_populates="posts")
    number = db.Column(db.String, nullable=False)
    text = db.Column(db.String)
    publication_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    comments = db.relationship("Comment", back_populates="post")
    analysis_data = db.relationship("AnalysisData", back_populates="post", uselist=False)

    def delete(self):
        self.is_deleted = True

    def __repr__(self):
        return f"Post id={self.id} text={self.text[:40]}"


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    post = db.relationship("Post", back_populates="comments")
    text = db.Column(db.String)
    number = db.Column(db.Integer)
    sentiment_color = db.Column(db.String)
    is_deleted = db.Column(db.Boolean, default=False)

    def delete(self):
        self.is_deleted = True

    def __repr__(self):
        return f"Comment id={self.id} text={self.text[:40]} sentiment_color={self.sentiment_color}"


class AnalysisData(db.Model):
    __tablename__ = "analysis_data"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    post = db.relationship("Post", back_populates="analysis_data")
    num_likes = db.Column(db.Integer)
    num_views = db.Column(db.Integer)
    num_comments = db.Column(db.Integer)
    sentiment_color = db.Column(db.String)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    def delete(self):
        self.is_deleted = True

    def __repr__(self):
        return f"AnalysisData id={self.id} analysis_date={self.analysis_date}"

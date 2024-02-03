from datetime import datetime
from tparser.db import db


class Channel(db.Model):
    __tablename__ = "channels"

    id = db.Column(db.Integer, primary_key=True)
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
    sentiment_color = db.Column(db.Float)
    is_deleted = db.Column(db.Boolean, default=False)

    def delete(self):
        self.is_deleted = True

    def get_sentiment_color(self):
        comments = Comment.query.filter(Comment.post_id == self.id).all()
        print("DEBUG:", comments)
        comments_colors = [comment.sentiment_color for comment in comments]
        sentiment_color = sum(comments_colors) / len(comments_colors)
        print("DEBUG:", sentiment_color)
        self.sentiment_color = sentiment_color

    def __repr__(self):
        return f"Post id={self.id} text={self.text[:40]}"


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    text = db.Column(db.String)
    number = db.Column(db.Integer)
    sentiment_color = db.Column(db.Float)
    is_deleted = db.Column(db.Boolean, default=False)

    def delete(self):
        self.is_deleted = True

    def __repr__(self):
        return f"Comment id={self.id} text={self.text[:40]} sentiment_color={self.sentiment_color}"

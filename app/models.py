# app/models.py

from app import db

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.article_id'), nullable=False)
    article = db.relationship('Article', backref=db.backref('comments', lazy=True))

class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.DateTime, default=db.func.current_timestamp())



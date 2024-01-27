# app/views.py

from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from app import api, db
from app.models import Article, Comment

article_fields = {
    'article_id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'author': fields.String,
    'publication_date': fields.DateTime(dt_format='iso8601'),
}

comment_fields = {
    'comment_id': fields.Integer,
    'author': fields.String,
    'content': fields.String,
}

class ArticlesResource(Resource):
    @marshal_with(article_fields)
    def get(self, article_id=None):
        # GET all articles or a specific article
        if article_id:
            article = Article.query.get(article_id)
            if not article:
                return {'message': 'Article not found'}, 404
            return article
        else:
            articles = Article.query.all()
            return articles

    @marshal_with(article_fields)
    def post(self):
        # POST: Create a new article
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title cannot be blank')
        parser.add_argument('content', type=str, required=True, help='Content cannot be blank')
        parser.add_argument('author', type=str, required=True, help='Author cannot be blank')
        args = parser.parse_args()

        new_article = Article(
            title=args['title'],
            content=args['content'],
            author=args['author']
        )

        db.session.add(new_article)
        db.session.commit()

        return new_article, 201

    @marshal_with(article_fields)
    def put(self, article_id):
        # PUT: Update an existing article
        article = Article.query.get(article_id)

        if not article:
            return {'message': 'Article not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('content', type=str)
        parser.add_argument('author', type=str)
        args = parser.parse_args()

        if args['title']:
            article.title = args['title']
        if args['content']:
            article.content = args['content']
        if args['author']:
            article.author = args['author']

        db.session.commit()

        return article

    def delete(self, article_id):
        # DELETE: Delete an article
        article = Article.query.get(article_id)

        if not article:
            return {'message': 'Article not found'}, 404

        db.session.delete(article)
        db.session.commit()

        return {'message': 'Article deleted successfully'}


api.add_resource(ArticlesResource, '/api/articles', '/api/articles/<int:article_id>')

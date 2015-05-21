#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import g
from flask import request
from flask.ext.restful import Resource

from models import db
from models import Column
from models import Article
from .token import auth


class ArticleListApi(Resource):

    @auth.login_required
    def get(self, website_id, column_id):
        _articles = Article.query.join(Column).filter(
            Column.website_id == website_id).filter(Column.id == column_id).all()
        _l = []
        for _article in _articles:
            _l.append(_article.to_dict())
        return _l

    @auth.login_required
    def post(self):
        _article = Article(title='test1', content='text1')
        db.session.add(_article)
        db.session.commit()
        return {'id': _article.id, 'title': _article.title, 'content': _article.content}, 201

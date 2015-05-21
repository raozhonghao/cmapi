#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from sqlalchemy.dialects.postgresql import UUID
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from itsdangerous import BadSignature

import app
db = app.get_db()


class IdAndToDictMixin(object):
    id = db.Column(UUID, primary_key=True, default=db.func.uuid_generate_v4())

    def to_dict(self):
        _d = {}
        for _column in self.__table__.columns:
            if getattr(self, _column.name):
                _d[_column.name] = str(getattr(self, _column.name))
                if '_id' in _column.name:
                    _c = _column.name[0: -3]
                    if hasattr(self, _c):
                        _o = getattr(self, _c)
                        if hasattr(_o, 'name'):
                            _d[_c] = _o.name
        return _d


class TimestampMixin(object):
    created_time = db.Column(db.DateTime, default=db.func.now())
    updated_time = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())


class Website(db.Model, IdAndToDictMixin):
    __tablename__ = 'websites'

    name = db.Column(db.String(40))


class User(db.Model, IdAndToDictMixin):
    __tablename__ = 'users'

    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    nickname = db.Column(db.String(40))
    is_root = db.Column(db.Boolean, default=False)
    website_id = db.Column(UUID, db.ForeignKey(
        'websites.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    website = db.relationship('Website', backref=db.backref('users'))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 1800):
        _s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        return _s.dumps({'id': self.id})

    @classmethod
    def verify_auth_token(cls, token):
        _s = Serializer(current_app.config['SECRET_KEY'])
        try:
            _data = _s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        _user = User.query.get(_data['id'])
        return _user


class Column(db.Model, IdAndToDictMixin):
    __tablename__ = 'columns'

    layer = db.Column(db.Integer)
    name = db.Column(db.String(20))
    parent = db.Column(db.String(20))
    website_id = db.Column(UUID, db.ForeignKey(
        'websites.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    website = db.relationship('Website', backref=db.backref('columns'))


class Article(db.Model, IdAndToDictMixin, TimestampMixin):
    __tablename__ = 'articles'

    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    column_id = db.Column(UUID, db.ForeignKey(
        'columns.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    column = db.relationship('Column', backref=db.backref('articles'))

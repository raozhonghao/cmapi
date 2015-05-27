#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
from flask.ext.restful import Resource
from sqlalchemy.exc import IntegrityError

from models import db
from models import Website
from models import Column
from .token import auth


class ColumnListApi(Resource):

    @auth.login_required
    def get(self, website_id):
        _columns = Column.query.filter_by(website_id=website_id).all()
        _l = []
        for _column in _columns:
            _d = _column.to_dict()
            _d['link'] =  '/websites/%s/columns/%s' % (website_id, _column.id)
            _l.append(_d)
        return _l, 200

    @auth.login_required
    def post(self, website_id):
        _args = request.json
        _name = _args.get('name', None)
        if not _name or len(_name) > 20:
            return {'status': 400, 'message': '请提供正确的栏目名称'}, 400
        _layer = int(_args.get('layer', 1))
        if not _layer:
            return {'status': 400, 'message': '请提供正确的栏目层级'}, 400
        _parent = _args.get('parent', None)
        _p_col = None
        if _layer > 1 and not _parent:
            return {'status': 400, 'message': '请提供正确的父级栏目名称'}, 400
        if _layer > 1 and _parent:
            _p_col = Column.query.filter_by(name=_parent).first()
            if not _p_col: 
                return {'status': 400, 'message': '找不到对应的父级栏目'}, 400
        _description = _args.get('description', None)
        _column = Column(name=_name, layer=_layer, parent=_parent, description=_description, website_id=website_id)
        db.session.add(_column)
        db.session.commit()
        return _column.to_dict(), 200


class ColumnApi(Resource):
    @auth.login_required
    def get(self, website_id, column_id):
        _column = Column.query.filter_by(id=column_id).first()
        _d = _column.to_dict()
        _d['articles'] = {'count': len(_column.articles), 'link': '/websites/%s/columns/%s/articles' % (website_id, _column.id)}
        return _d, 200

    @auth.login_required
    def delete(self, website_id, column_id):
        _column = Column.query.get(column_id)
        db.session.delete(_column)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'status': 400, 'message': 'If you want to delete the column "%s", please delete all articles belong to it before.' % (_column.name)}, 400
        return {}, 204

    @auth.login_required
    def put(self, website_id, column_id):
        _column = Column.query.get(column_id)
        _description = request.json.get('description', None)
        if _description:
            _column.description = _description
            db.session.commit()
        _d = _column.to_dict()
        _d['articles'] = {'count': len(_column.articles), 'link': '/websites/%s/columns/%s/articles' % (website_id, _column.id)}
        return _d, 200


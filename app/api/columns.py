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
            _d['link'] =  '/websites/%s/columns' % (website_id)
            _l.append(_d)
        return _l, 200


class ColumnApi(Resource):

    def delete(self, id):
        _column = Column.query.get(id)
        db.session.delete(_column)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'status': 400, 'message': 'If you want to delete the column "%s", please delete all articles belong to it before.' % (_column.name)}, 400
        return {'message': 'The column "%s" has been deleted' % (_column.name)}, 200

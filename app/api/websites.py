#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import g
from flask import request
from flask.ext.restful import Resource
from sqlalchemy.exc import IntegrityError

from models import db
from models import Website
from .token import auth


class WebsiteListApi(Resource):

    @auth.login_required
    def get(self):
        _user = g.user
        _l = []
        if not _user.is_root:
            _l.append(_user.website.to_dict())
        else:
            _websites = Website.query.all()
            for _w in _websites:
                _l.append(_w.to_dict())
        return _l, 200

class WebsiteApi(Resource):
    @auth.login_required
    def get(self, website_id):
        _website = Website.query.filter_by(id=website_id).first()
        _d = _website.to_dict()
        _d['columns'] = {'count': len(_website.columns), 'link': '/websites/%s/columns' % (website_id)}
        return _d, 200

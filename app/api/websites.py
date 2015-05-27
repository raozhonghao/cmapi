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
            _d = _user.website.to_dict()
            _d['link'] = '/websites/%s' % _user.website.id
            _l.append(_d)
        else:
            _websites = Website.query.all()
            for _website in _websites:
                _d = _website.to_dict()
                _d['link'] = '/websites/%s' % _website.id
                _l.append(_d)
        return _l, 200

    @auth.login_required
    def post(self):
        _user = g.user
        if not _user.is_root:
            return {'status': 400, 'message': '需要系统管理员权限'}, 400
        _name = request.json.get('name', None)
        if not _name or len(_name) > 40:
            return {'status': 400, 'message': '请提供正确的网站名称'}, 400
        _website = Website(name=_name)
        db.session.add(_website)
        db.session.commit()
        return _website.to_dict(), 201

class WebsiteApi(Resource):
    @auth.login_required
    def get(self, website_id):
        _user = g.user
        _website = Website.query.filter_by(id=website_id).first()
        _d = _website.to_dict()
        _d['columns'] = {'count': len(_website.columns), 'link': '/websites/%s/columns' % (website_id)}
        if _user.is_root:
            _d['removable'] = True
        return _d, 200

    @auth.login_required
    def delete(self, website_id):
        _user = g.user
        if not _user.is_root:
            return {'status': 400, 'message': 'You are not an administrator'}, 400
        _website = Website.query.get(website_id)
        db.session.delete(_website)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'status': 400, 'message': 'If you want to delete the website "%s", please delete all users and columns belong to it before.' % (_website.name)}, 400
        return {}, 204

    @auth.login_required
    def put(self, website_id):
        _user = g.user
        _website = Website.query.get(website_id)
        _description = request.json.get('description', None)
        if _description:
            _website.description = _description
            db.session.commit()
        _d = _website.to_dict()
        _d['columns'] = {'count': len(_website.columns), 'link': '/websites/%s/columns' % (website_id)}
        if _user.is_root:
            _d['removable'] = True
        return _d, 200


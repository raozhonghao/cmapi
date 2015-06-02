#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
from flask.ext.restful import Resource

from models import db
from models import User
from models import Website


class UserListApi(Resource):

    def get(self):
        pass

    def post(self):
        _username = request.json.get('username', None)
        _password = request.json.get('password', None)
        _nickname = request.json.get('nickname', None)
        _website_name = request.json.get('website', None)
        if not _username:
            return {'status': 400, 'message': 'No username provided'}, 400
        if not _password:
            return {'status': 400, 'message': 'No password provided'}, 400
        if not _website_name:
            return {'status': 400, 'message': 'No website provided'}, 400
        _website = Website.query.filter_by(name=_website_name).first()
        if not _website:
            return {'status': 404, 'message': 'Website %s is not found' % (_website_name)}, 404
        _user = User(
            username=_username, nickname=_nickname, website_id=_website.id)
        _user.hash_password(_password)
        db.session.add(_user)
        db.session.commit()
        _d = _user.to_dict()
        _d.pop("password_hash")
        return _d, 201


class UserApi(Resource):

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

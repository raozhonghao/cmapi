#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import current_app
from flask import request
from flask import g
from flask.ext.restful import Resource
from flask.ext.httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from models import db
import logging

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    from models import User
    _user = User.verify_auth_token(username_or_token)
    if not _user:
        _user = User.query.filter_by(username=username_or_token).first()
        if not _user or not _user.verify_password(password):
            return False
    else:
        g.token = username_or_token
    g.user = _user
    return True
    
class TokenApi(Resource):
    @auth.login_required
    def get(self):
        if hasattr(g, 'token'):
            return {'token': g.token}, 200
        _token = g.user.generate_auth_token(current_app.config['EXPIRES_IN'])
        return {'token': _token.decode('ascii')}, 200

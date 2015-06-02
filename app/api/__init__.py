#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import g
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    from models import User
    _user = User.query.filter_by(username=username).first()
    if not _user or not _user.verify_password(password):
        return False
    g.user = _user
    return True

#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://xuanye:xuanye0309@127.0.0.1:5432/content_management'
    SECRET_KEY = 'v8We5m27Bcn903yn'
    EXPIRES_IN = 1800


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass

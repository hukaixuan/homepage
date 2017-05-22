# coding:utf-8
import os
import redis

class Config:
    base_dir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:'+os.environ.get('MYSQL_PWD')+'@localhost/homepage?charset=utf8mb4'
    USE_TOKEN_AUTH = True

    # enable rate limits only if redis is running
    try:
        r = redis.Redis()
        r.ping()
        print('redis server is running...\n use rate limits')
        USE_RATE_LIMITS = True
    except redis.ConnectionError:
        USE_RATE_LIMITS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    USE_TOKEN_AUTH = True
    USE_RATE_LIMITS = False


class ProducitonConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProducitonConfig,

    'default': DevelopmentConfig
}






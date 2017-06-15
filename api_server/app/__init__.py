import os
from flask import Flask
from .models import db
from .auth import auth
from .decorators import json, etag
from .errors import not_found, not_allowed
from config import config
from flask_cors import CORS, cross_origin


def create_app(config_name=None):
    app = Flask(__name__)
    CORS(app)
    if not config_name:
        config_name='default'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    from .api.v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    if app.config['USE_TOKEN_AUTH']:
        from .token import token as token_blueprint
        app.register_blueprint(token_blueprint, url_prefix='/auth')

    @app.route('/')
    @auth.login_required
    @etag
    @json
    def index():
        from .api.v1 import get_catalog as v1_catalog
        return {'versions': {'v1': v1_catalog()}}

    @app.errorhandler(404)
    @auth.login_required
    def not_found_error(e):
        return not_found('item not found')

    @app.errorhandler(405)
    def method_not_allowed_error(e):
        return not_allowed()

    return app



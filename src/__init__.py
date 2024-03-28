from logging.handlers import RotatingFileHandler
import os
import logging
from flask import Flask, _app_ctx_stack, jsonify
from sebi_lib.utils import get_database_scoped_session
from .flask_helper import *
from sqlalchemy import orm
import yaml
from .finalyca_json_encoder import FinalycaJSONEncoder

def create_app(yaml_config_path):
    app = Flask(__name__)

    app.json_encoder = FinalycaJSONEncoder

    # handler = RotatingFileHandler(os.path.join(app.root_path, '../logs', 'log.log'), maxBytes=102400, backupCount=10)
    # logging_format = logging.Formatter(
    # '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    # handler.setFormatter(logging_format)
    # app.logger.addHandler(handler)

    with open(yaml_config_path) as conf_file:
        config = yaml.load(conf_file, Loader=yaml.FullLoader)

    app.db = get_database_scoped_session(config['DB_URI'])

    app.before_request(fn_before_request)
    app.after_request(fn_after_request)
    app.teardown_request(fn_teardown_request)
    
    # app.register_error_handler(Exception, exception_jsonifier)

    from sebi_lib.api import api_bp
    with app.app_context():
        app.register_blueprint(api_bp)

    @app.route("/")
    def index():
        return jsonify({"msg": "I am alive"})
    return app

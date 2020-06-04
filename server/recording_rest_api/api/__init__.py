from recording_rest_api.api.endpoint_recording import ns as recording_namespace
from recording_rest_api.api.endpoint_controll import ns as controll_namespace
from recording_rest_api.api.restplus import api
from recording_rest_api.database import db
from recording_rest_api import app
from flask import Blueprint
import logging

log = logging.getLogger(__name__)


def initialize_app():
    log.info("Init Flaskapp")
    app.config.from_object('configs.webapp')
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(recording_namespace)
    api.add_namespace(controll_namespace)
    app.register_blueprint(blueprint)
    db.init_app(app)

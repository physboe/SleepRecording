from flask import Flask, Blueprint
from recording_rest_api.api.recording import ns as recording_namespace
from recording_rest_api.api.restplus import api

app = Flask(__name__, instance_relative_config=True)


def initialize_app():
    app.config.from_object('configs.webapp')
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(recording_namespace)
    app.register_blueprint(blueprint)

    #db.init_app(flask_app)

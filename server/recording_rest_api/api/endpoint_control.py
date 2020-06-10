import logging
from flask_restplus import Resource
from recording_rest_api.api.restplus import api
from recording_rest_api import database
from recording_rest_api.api.models import pingResponse

log = logging.getLogger(__name__)
ns = api.namespace('test', description='Operations related to administrate')


@ns.route('/install')
class Install(Resource):

    def get(self):
        database.reset_database()


@ns.route('/')
class Ping(Resource):

    @api.marshal_with(pingResponse)
    def get(self):
        log.info(f"ping from ")
        return True, 201

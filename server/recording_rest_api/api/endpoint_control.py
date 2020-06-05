import logging
from flask_restplus import Resource
from recording_rest_api.api.restplus import api
from recording_rest_api import database

log = logging.getLogger(__name__)

ns = api.namespace('ping', description='Operations related to handle hrm loggings')


@ns.route('/install')
class Install(Resource):

    def get(self):
        database.reset_database()

@ns.route('/')
@api.response(201, 'Ping successfull')
class Ping(Resource):

    def get(self):
        log.info(f"ping from ")

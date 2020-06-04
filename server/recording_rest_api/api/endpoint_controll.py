import logging
from flask_restplus import Resource
from recording_rest_api.api.restplus import api
from recording_rest_api import database

log = logging.getLogger(__name__)

ns = api.namespace('controll', description='Operations related to handle hrm loggings')


@ns.route('/install')
class Install(Resource):

    def get(self):
        database.reset_database()
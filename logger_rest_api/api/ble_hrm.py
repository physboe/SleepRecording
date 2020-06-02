import logging
from flask import request
from flask_restplus import Resource
from logger_rest_api.api.restplus import api
from logger_rest_api.api.serializers import  recordingState
from logger_rest_api.services.hrm import HrmService

log = logging.getLogger(__name__)

ns = api.namespace('hrm', description='Operations related to handle hrm loggings')


@ns.route('/')
class BleHrmRerding(Resource):


    @api.response(201, 'Recording successfully started.')
    @api.expect(recordingState)
    def put(self):
        """
        Creates a new blog category.
        """
        if request.json.get('running'):
            HrmService().startRecording()
        else:
            HrmService().stopRecording()
        return None, 201

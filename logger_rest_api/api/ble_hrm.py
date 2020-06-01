import logging
from flask import request
from flask_restplus import Resource
from logger_rest_api.api.restplus import api
from logger_rest_api.api.serializers import startRecording, stopRecording
from logger_rest_api.services.hrm import HrmService

log = logging.getLogger(__name__)

ns = api.namespace('hrm', description='Operations related to handle hrm loggings')


@ns.route('/')
class BleHrmRerding(Resource):

#    def __init__(self):
#        log.debug("init")
#        self.__hrmservice = HrmService()

    @api.response(201, 'Recording successfully started.')
    @api.expect(startRecording)
    def post(self):
        """
        Creates a new blog category.
        """
        log.debug("recording start")

        HrmService().startRecording()
        return None, 201

    @api.response(201, 'Recording successfully started.')
    @api.expect(stopRecording)
    def put(self):
        """
        Creates a new blog category.
        """
        HrmService().stopRecording()
        return None, 201

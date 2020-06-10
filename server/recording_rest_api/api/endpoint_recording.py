import logging
from flask import request
from flask_restplus import Resource
from recording_rest_api.api.restplus import api
from recording_rest_api.api.models import recordingState
from recording_rest_api.services.manager import RecordingManager
from recording_rest_api.database.recording import RecordingState

log = logging.getLogger(__name__)

ns = api.namespace('recording', description='Operations related recording')


@ns.route('/')
class Recording(Resource):

    @api.marshal_with(recordingState)
    @api.expect(recordingState)
    def put(self):
        """
        Starts de recordings.
        """
        if request.json.get('running'):
            RecordingManager().startRecordings(request.json.get('tag'))
        else:
            RecordingManager().stopRecordings()
        return RecordingState(RecordingManager().isRecording()), 201

    @api.marshal_with(recordingState)
    def get(self):
        return RecordingState(RecordingManager().isRecording())

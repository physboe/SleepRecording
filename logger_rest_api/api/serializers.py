from flask_restplus import fields
from logger_rest_api.api.restplus import api


recordingState = api.model('RecordingState', {
    'running': fields.Boolean(required=True),
})

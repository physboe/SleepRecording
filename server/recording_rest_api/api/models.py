from flask_restplus import fields
from recording_rest_api.api.restplus import api


recordingState = api.model('RecordingState', {
    'RecordingState': {
        'running': fields.Boolean(required=True),
        'tag': fields.String(required=False)
    }
})

pingResponse = api.model('PingReponse', {
    'ping': fields.Boolean(default=True)
})

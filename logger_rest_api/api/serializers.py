from flask_restplus import fields
from logger_rest_api.api.restplus import api


startRecording = api.model('StartRecording', {
})

stopRecording = api.model('StopRecording', {
})

import logging
from flask_restplus import Api
from BLEHeartRate import ConnectionFailed

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Ble Hrm Api',
          description='To Start and Stop the Hrm Recording')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    return {'message': message}, 500


@api.errorhandler(ConnectionFailed)
def deivce_not_connected_error_handler(e):
    return {'message': f'Could not connect  {e.deviceMAc}'}, 404

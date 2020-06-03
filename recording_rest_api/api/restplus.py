import logging
from flask_restplus import Api

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Ble Hrm Api',
          description='To Start and Stop the Hrm Recording')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    return {'message': message}, 500

import logging
import traceback

from flask_restplus import Api
from logger_rest_api import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Ble Hrm Api',
          description='To Start and Stop the Hrm Recording')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500

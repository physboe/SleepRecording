
from recording_rest_api import api
from recording_rest_api import app
import os
import logging.config

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'configs/logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    api.initialize_app()
    #    app.run(host='0.0.0.0', ssl_context=('cert/cert.pem', 'cert/key.pem'))
    app.run(host='0.0.0.0')

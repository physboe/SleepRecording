
import logging.config
import os
from recording_rest_api import api
from recording_rest_api import app

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'configs/logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def main():
    api.initialize_app()
    app.run(host='0.0.0.0', ssl_context=('cert/cert.pem', 'cert/key.pem'))


if __name__ == "__main__":
    main()

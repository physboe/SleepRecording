
import logging.config
import os
from recording_rest_api import api
from recording_rest_api import app
from configs import webapp as config

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'configs/logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def main():
    log.info(f'>> Starting development server at http://{config.SERVER_NAME}/api/ <<')
    api.initialize_app()
    app.run()



if __name__ == "__main__":
    main()

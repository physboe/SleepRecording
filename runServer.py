
import logging.config
import os
import recording_rest_api as webapp
from recording_rest_api import app as flaskapp

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'configs/logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def main():
    webapp.initialize_app()
    log.info(flaskapp.config)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(flaskapp.config['SERVER_NAME']))
    flaskapp.run()

if __name__ == "__main__":
    main()

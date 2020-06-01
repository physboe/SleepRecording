import logging.config
from ble_hrm_logger import CLIUtils as cliu
from ble_hrm_logger import BLEHeartRate as ble
from ble_hrm_logger import DatabaseLayer as dbl
import os
import sys

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../configs/logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

def init():
    """
    Entry point for the command line interface
    """
    try:
        log.info("start application")
        confpath = os.path.join("configs", "SuuntoLocal.conf")
        args = cliu.loadConfigParameter(confpath)
        databaselayer = dbl.DatabaseService(args.o)
        gatttoolutil = ble.BLEHearRateService(args.g, args.d)
        try:
            gatttoolutil.connectToDevice(args.m, args.t)
            gatttoolutil.registeringToHrHandle()
            gatttoolutil.startRecording(databaselayer)
        except KeyboardInterrupt as key:
            log.exception(key, exc_info=True)

        except Exception as e:
            log.exception(e, exc_info=True)
        finally:
            gatttoolutil.close()

    except Exception as e:
        logging.exception(e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    init()

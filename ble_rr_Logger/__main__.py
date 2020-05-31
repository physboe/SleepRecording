import logging
from ble_rr_Logger import ConfigLoader as config
from ble_rr_Logger import LoggingUtils as loggingutils
from ble_rr_Logger import BLEHeartRateService as ble
from ble_rr_Logger import DatabaseLayer as dbl
import os
import sys


def init():
    """
    Entry point for the command line interface
    """
    loggingutils.initLogging()
    try:
        logging.info("command line interface")
        confpath = os.path.join("configs", "SuuntoLocal.conf")
        args = config.loadConfigParameter(confpath)
        loggingutils.setLoggingStage(args.v)
        databaselayer = dbl.DatabaseLayer(args.o)
        try:

            gatttoolutil = ble.BLEHearRateService(args.g, databaselayer)
        except Exception as e:
            logging.exception(e, exc_info=True)
            sys.exit(1)
        finally:
            databaselayer.close()

    except Exception as e:
        logging.exception(e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    init()

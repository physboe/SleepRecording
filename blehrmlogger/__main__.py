import logging
from blehrmlogger import ConfigLoader as config
from blehrmlogger import LoggingUtils as loggingutils
from blehrmlogger import BLEHeartRateService as ble
from blehrmlogger import DatabaseLayer as dbl
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
        gatttoolutil = ble.BLEHearRateService(args.g, databaselayer, args.d)
        try:
            gatttoolutil.connectToDevice(args.m, args.t)
            gatttoolutil.registeringToHrHandle()
            gatttoolutil.listenToNotification(None)
        except KeyboardInterrupt as key:
            logging.exception(key, exc_info=True)
            gatttoolutil.close()

        except Exception as e:
            logging.exception(e, exc_info=True)
        finally:
            databaselayer.close()
            gatttoolutil.close()

    except Exception as e:
        logging.exception(e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    init()

import logging
from blehrmlogger import CLIUtils as cliu
from blehrmlogger import BLEHeartRateService as ble
from blehrmlogger import DatabaseLayer as dbl
import os
import sys

LOGGING_FORMAT = "%(asctime)s:%(module)s:%(funcName)s:%(levelname)s: %(message)s"

def init():
    """
    Entry point for the command line interface
    """
    try:
        logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)
        confpath = os.path.join("configs", "SuuntoLocal.conf")
        args = cliu.loadConfigParameter(confpath)
        databaselayer = dbl.DatabaseLayer(args.o)
        gatttoolutil = ble.BLEHearRateService(args.g, args.d)
        try:
            gatttoolutil.connectToDevice(args.m, args.t)
            gatttoolutil.registeringToHrHandle()
            gatttoolutil.startRecording(databaselayer)
        except KeyboardInterrupt as key:
            logging.exception(key, exc_info=True)

        except Exception as e:
            logging.exception(e, exc_info=True)
        finally:
            gatttoolutil.close()

    except Exception as e:
        logging.exception(e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    init()

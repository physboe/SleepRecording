import logging
from ble_rr_Logger import ConfigLoader as config
from ble_rr_Logger import LoggingUtils as loggingutils
from ble_rr_Logger import GatttoolUtil as gatt
import os
import sys


def init():
    """
    Entry point for the command line interface
    """
    loggingutils.initLogging()
    try:
        logging.info("command line interface")
        confpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "/config/SuuntoLocal.conf")
        args = config.loadConfigParameter(confpath)
        loggingutils.setLoggingStage(args)
        gatttoolutil = gatt.GatttoolUtil(args.g)
    except Exception as e:
        logging.error("Theres an error: {}".format(e.message))
        sys.exit(1)


    # Increase verbose level


    #main(args.m, args.o, args.g, args.b, args.H, args.d)




if __name__ == "__main__":
    init()

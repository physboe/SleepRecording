import logging


def initLogging():
    logging.basicConfig(level=logging.DEBUG)


def setLoggingStage(debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

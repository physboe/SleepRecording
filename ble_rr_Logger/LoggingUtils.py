import logging


def initLogging():
    logging.basicConfig(level=logging.DEBUG)


def setLoggingStage(args):
    if args.v:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

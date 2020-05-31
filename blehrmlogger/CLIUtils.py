import argparse
import logging
import os
import configparser


def initLogging():
    logging.basicConfig(format="%(asctime)s:%(module)s:%(funcName)s:%(levelname)s: %(message)s",level=logging.DEBUG)


def setLoggingStage(debug):
    logging.debug("Debuggng: " + str(debug))
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def createParser():
    parser = argparse.ArgumentParser(description="Bluetooth heart rate monitor data logger")
    parser.add_argument("-m", metavar='MAC', type=str, help="MAC address of BLE device (default: auto-discovery)")
    parser.add_argument("-g", metavar='PATH', type=str, help="gatttool path (default: system available)", default="gatttool")
    parser.add_argument("-o", metavar='FILE', type=str, help="Output filename of the database (default: none)")
    parser.add_argument("-H", metavar='HR_HANDLE', type=str, help="Gatttool handle used for HR notifications (default: none)")
    parser.add_argument("-v", action='store_true', help="Verbose output", default=False)
    parser.add_argument("-d", action='store_true', help="Enable debug of gatttool")
    parser.add_argument("-t", metavar='TYPE', type=str, help="Connection type random or public")
    return parser


def loadConfigParameter(confpath):
    parser = createParser()

    if os.path.exists(confpath):
        logging.debug("Config File found: " + os.path.abspath(confpath))
        config = configparser.ConfigParser()
        config.read([confpath])
        config = dict(config.items("config"))

        # We compare here the configuration given in the config file with the
        # configuration of the parser.
        args = vars(parser.parse_args([]))
        err = False
        for key in config.keys():
            if key not in args:
                logging.error("Configuration file error: invalid key '" + key + "'.")
                err = True
        if err:
            raise KeyError("Configuration file error'")
        parser.set_defaults(**config)
    return parser.parse_args()

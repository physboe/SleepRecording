import os
import logging

class GatttoolUtil:

    def __init__(self, argsG):
        if argsG != "gatttool" and not os.path.exists(argsG):
            logging.critical("Couldn't find gatttool path!")
            raise RuntimeError("No Gatttool found")

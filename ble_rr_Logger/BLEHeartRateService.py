import os
import logging


class BLEHearRateService:

    def __init__(self, gatttoolpath, recordimpl):
        if gatttoolpath != "gatttool" and not os.path.exists(gatttoolpath):
            logging.critical("Couldn't find gatttool path!")
            raise RuntimeError("No Gatttool found")

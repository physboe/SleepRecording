import os
import logging
import pexpect
import sys


class BLEHearRateService:

    def __init__(self, gatttoolpath, recordimpl, debug):
        if gatttoolpath != "gatttool" and not os.path.exists(gatttoolpath):
            logging.critical("Couldn't find gatttool path!")
            raise RuntimeError("No Gatttool found")
        self.__debug = debug
        self.__run = True
        self.__gatttoolpath = gatttoolpath

    def connectToDevice(self, deviceMAC, connectionType):
        while self.__run:
            logging.info("Establishing connection to " + deviceMAC)
            self.__gatttool = pexpect.spawn(self.__gatttoolpath + " -b " + deviceMAC + " -t " + connectionType +" --interactive")
            if self.__debug:
                self.__gatttool.logfile = sys.stdout ### ins logging

            self.__gatttool.expect(r"\[LE\]>")
            self.__gatttool.sendline("connect")

            try:
                i = self.__gatttool.expect(["Connection successful.", r"\[CON\]"], timeout=30)
                if i == 0:
                    self.__gatttool.expect(r"\[LE\]>", timeout=30)

            except pexpect.TIMEOUT:
                logging.info("Connection timeout. Retrying.")
                continue

            logging.info("Connected to " + deviceMAC)
            break

    def close(self):
        self.__run = False
        logging.info("Clonntion closing")

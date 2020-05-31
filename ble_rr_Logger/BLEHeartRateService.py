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
            gt = pexpect.spawn(self.__gatttoolpath + " -b " + deviceMAC + " -t " + connectionType +" --interactive")
            if self.__debug:
                gt.logfile = sys.stdout ### ins logging

            gt.expect(r"\[LE\]>")
            gt.sendline("connect")

            try:
                i = gt.expect(["Connection successful.", r"\[CON\]"], timeout=30)
                if i == 0:
                    gt.expect(r"\[LE\]>", timeout=30)

            except pexpect.TIMEOUT:
                logging.info("Connection timeout. Retrying.")
                continue

            break

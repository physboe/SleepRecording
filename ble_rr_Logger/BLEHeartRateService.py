import os
import logging
import pexpect
import


class BLEHearRateService:

    def __init__(self, gatttoolpath, recordimpl, debug):
        if gatttoolpath != "gatttool" and not os.path.exists(gatttoolpath):
            logging.critical("Couldn't find gatttool path!")
            raise RuntimeError("No Gatttool found")
        self.__debug = debug
        self.__run = True

    def connectToDevice(self, deviceMAC, connectionType):
        while self.__run:
            logging.info("Establishing connection to " + addr)
            gt = pexpect.spawn(gatttool + " -b " + addr + " -t public --interactive")
            if self.__debug:
                gt.logfile = sys.stdout ### ins logging

            gt.expect(r"\[LE\]>")
            gt.sendline("connect")

            try:
                i = gt.expect(["Connection successful.", r"\[CON\]"], timeout=30)
                if i == 0:
                    gt.expect(r"\[LE\]>", timeout=30)

            except pexpect.TIMEOUT:
                log.info("Connection timeout. Retrying.")
                continue

            break

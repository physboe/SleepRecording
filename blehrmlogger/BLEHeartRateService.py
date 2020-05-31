import os
import logging
import pexpect
import sys


class BLEHearRateService:

    self.HRM_UUID = "00002a37"

    def __init__(self, gatttoolpath, recordimpl, debug):
        if gatttoolpath != "gatttool" and not os.path.exists(gatttoolpath):
            logging.critical("Couldn't find gatttool path!")
            raise RuntimeError("No Gatttool found")
        self.__debug = debug
        self.__run = True
        self.__gatttoolpath = gatttoolpath
        self.__connected = False

    def connectToDevice(self, deviceMAC, connectionType):
        if (self.__connected):
            logging.warning("Device already connected")
        else:
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

                self.__connected = True
                logging.info("Connected to " + deviceMAC)
                break

    def registeringToHrHandle(self):
        if self.__connected:
            self.__gatttool.sendline("char-desc")
            while self.__run:
                try:
                    self.__getttool.expect(r"handle: (0x[0-9a-f]+), uuid: ([0-9a-f]{8})", timeout=10)
                except pexpect.TIMEOUT:
                    break

                handle = self.__getttool.match.group(1).decode()
                uuid = self.__getttool.match.group(2).decode()

                if uuid == self.HRM_UUID:
                    hr_handle = handle
                    break

            if hr_handle is None:
                logging.error("Couldn't find the heart rate measurement handle?!")
                raise HrmHandleNotFoundError(self.HRM_UUID)
            logging.info("Handle: " + hr_handle)
            return hr_handle

        else:
            raise NoDeviceConnected()

    def close(self):
        self.__run = False
        if self.__connected:
            self.__gatttool.sendline("exit")
            self.__connected = False
        logging.info("Connection closing")


class HrmHandleNotFoundError(Exception):
    pass


class NoDeviceConnected(Exception):
    pass

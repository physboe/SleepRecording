import os
import logging
import pexpect
import sys


class BLEHearRateService:

    HRM_UUID = "00002a37"

    def __init__(self, gatttoolpath, recordimpl, debug):
        if gatttoolpath != "gatttool" and not os.path.exists(gatttoolpath):
            logging.critical("Couldn't find gatttool path!")
            raise RuntimeError("No Gatttool found")
        self.__debug = debug
        self.__run = True
        self.__gatttoolpath = gatttoolpath
        self.__connected = False
        self.__registered = False

    def connectToDevice(self, deviceMAC, connectionType):
        if self.__connected:
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

    def listenToNotification(self, Listener):
        if self.__connected and self.__registered:

            notification_expect = "Notification handle = " + self.__handle + " value: ([0-9a-f ]+)"

            while self.__run:
                try:
                    self.__gatttool.expect(notification_expect, timeout=10)
                    datahex = self.__gatttool.match.group(1).strip()
                    data = map(lambda x: int(x, 16), datahex.split(b' '))
                    logging.info("Handle Notification")
                #    res = interpret(list(data))
                except pexpect.TIMEOUT:
                    logging.warn("Connection lost with ")
                    raise ConnectionLostError("Connection lost with ")

        else:
            raise NoDeviceConnectedError("No Device connected or no Handle registered")

    def registeringToHrHandle(self):
        if self.__connected:
            handle = self.__lookingForHandle()
            self.__gatttool.sendline("char-write-req " + handle + " 0100")
            self.__registered = True
            self.__handle = handle
            logging.info("Registered to Handle " + handle)
        else:
            raise NoDeviceConnectedError()

    def __lookingForHandle(self):
        self.__gatttool.sendline("char-desc")
        while self.__run:
            try:
                self.__gatttool.expect(r"handle: (0x[0-9a-f]+), uuid: ([0-9a-f]{8})", timeout=10)
            except pexpect.TIMEOUT:
                break

            handle = self.__gatttool.match.group(1).decode()
            uuid = self.__gatttool.match.group(2).decode()

            if uuid == self.HRM_UUID:
                self.__gatttool.expect(r"handle: (0x[0-9a-f]+), uuid: ([0-9a-f]{8})", timeout=10)
                handle = self.__gatttool.match.group(1).decode()
                hr_handle = handle
                break

        if hr_handle is None:
            logging.error("Couldn't find the heart rate measurement handle?!")
            raise HrmHandleNotFoundError(self.HRM_UUID)
        logging.info("Found Handle: " + hr_handle)
        return hr_handle

    def close(self):
        self.__run = False
        if self.__connected:
            self.__gatttool.sendline("quit")
            self.__gatttool.wait()
            self.__connected = False
            self.__registered = False
        logging.info("Connection closing")


class HrmHandleNotFoundError(Exception):
    pass


class NoDeviceConnectedError(Exception):
    pass


class ConnectionLostError(Exception):
    pass

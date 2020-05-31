import os
import logging
import pexpect
import sys
import abc
import time


class BLEHearRateService:

    HRM_UUID = "00002a37"
    RESULT_RR_INTERVAL_AVAILABLE = "rr_avb"
    RESULT_RR_INTERVAL = "rr"
    RESULT_HR = "hr"
    RESULT_SENSOR_CONTACT = "sensor_cont"
    RESULT_EE_STATUS = "ee_status"
    RESULT_EE = "ee"
    RESULT_HRV_UINT8 = "hrv_uint8"

    def __init__(self, gatttoolpath, debug):
        if gatttoolpath != "gatttool" and not os.path.exists(gatttoolpath):
            logging.critical("Couldn't find gatttool path!")
            raise RuntimeError("No Gatttool found")
        self.__debug = debug
        self.__gatttoolpath = gatttoolpath

        self.__setInitStat()
        self.__run = True

    def connectToDevice(self, deviceMAC, connectionType):
        if self.__connected:
            logging.warning("Device already connected")
        else:
            while self.__run:
                logging.info("Establishing connection to " + deviceMAC)
                self.__gatttool = pexpect.spawn(self.__gatttoolpath + " -b " + deviceMAC + " -t " + connectionType +" --interactive")
                if self.__debug:
                    self.__gatttool.logfile = sys.stdout.buffer ### ins logging

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

    def startRecording(self, logger):
        if self.__connected and self.__registered:
            self.__logger = logger
            self.__recordSession = logger.startRecordSession(self.__getTimeStamp())
            self.__recording = True

            notification_expect = "Notification handle = " + self.__handle + " value: ([0-9a-f ]+)"
            logging.info("Listen : " + notification_expect)
            while self.__run:
                try:
                    self.__gatttool.expect(notification_expect, timeout=10)
                    datahex = self.__gatttool.match.group(1).strip()
                    data = map(lambda x: int(x, 16), datahex.split(b' '))
                    result = self.__interpret(list(data))
                    self.__sendToDataLogger(result)
                    logging.info("Handle Notification: " + str(result))
                except pexpect.TIMEOUT:
                    logging.warn("Connection lost")

                    raise ConnectionLostError("Connection lost")

        else:
            raise NoDeviceConnectedError("No Device connected or no Handle registered")

    def registeringToHrHandle(self):
        if self.__connected:
            hr_handle, hr_handle_ctl = self.__lookingForHandle()
            self.__gatttool.sendline("char-write-req " + hr_handle_ctl + " 0100")
            self.__registered = True
            self.__handle = hr_handle
            logging.info("Registered to Handle " + hr_handle)
        else:
            raise NoDeviceConnectedError()

    def stopRecording(self):
        if self.__recording:
            self.__logger.stopRecordSession(self.__recordSession, self.__getTimeStamp())
            self.__recording = False

    def close(self):
        if self.__recording:
            self.stopRecording()

        self.__run = False
        if self.__connected:
            self.__gatttool.sendline("quit")
            self.__gatttool.wait()

        self.__setInitStat()
        logging.info("Connection closing")

    def __setInitStat(self):
        self.__run = False
        self.__connected = False
        self.__registered = False
        self.__recording = False
        self.__recordSession = None
        self.__logger = None
        self.__handle = None


    def __getTimeStamp(self):
        return int(time.time())

    def __sendToDataLogger(self, result):
        if result[self.RESULT_RR_INTERVAL_AVAILABLE]:
            for rrInterval in result[self.RESULT_RR_INTERVAL]:
                self.__logger.saveHrmData(self.__recordSession, result[self.RESULT_HR], rrInterval, result[self.RESULT_SENSOR_CONTACT], self.__getTimeStamp())
        else:
            self.__logger.saveHrmData(self.__recordSession, result[self.RESULT_HR], None, result[self.RESULT_SENSOR_CONTACT], self.__getTimeStamp())

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
                hr_handle = handle
                self.__gatttool.expect(r"handle: (0x[0-9a-f]+), uuid: ([0-9a-f]{8})", timeout=10)
                hr_handle_ctl = self.__gatttool.match.group(1).decode()
                break

        if hr_handle is None:
            logging.error("Couldn't find the heart rate measurement handle?!")
            raise HrmHandleNotFoundError(self.HRM_UUID)
        logging.info("Found Handle: " + hr_handle)
        return hr_handle, hr_handle_ctl

    def __interpret(self, data):

        byte0 = data[0]
        res = {}
        res[self.RESULT_HRV_UINT8] = (byte0 & 1) == 0
        sensor_contact = (byte0 >> 1) & 3
        if sensor_contact == 2:
            res[self.RESULT_SENSOR_CONTACT] = "No contact detected"
        elif sensor_contact == 3:
            res[self.RESULT_SENSOR_CONTACT] = "Contact detected"
        else:
            res[self.RESULT_SENSOR_CONTACT] = "Sensor contact not supported"
        res[self.RESULT_EE_STATUS] = ((byte0 >> 3) & 1) == 1
        res[self.RESULT_RR_INTERVAL_AVAILABLE] = ((byte0 >> 4) & 1) == 1

        if res[self.RESULT_HRV_UINT8]:
            res[self.RESULT_HR] = data[1]
            i = 2
        else:
            res[self.RESULT_HR] = (data[2] << 8) | data[1]
            i = 3

        if res[self.RESULT_EE_STATUS]:
            res[self.RESULT_EE] = (data[i + 1] << 8) | data[i]
            i += 2

        if res[self.RESULT_RR_INTERVAL_AVAILABLE]:
            res[self.RESULT_RR_INTERVAL] = []
            while i < len(data):
                # Note: Need to divide the value by 1024 to get in seconds
                res[self.RESULT_RR_INTERVAL].append((data[i + 1] << 8) | data[i])
                i += 2

        return res


class RecordingLoggerInterface(abc.ABC):

    @abc.abstractclassmethod
    def __init__(self):
        pass

    @abc.abstractclassmethod
    def startRecordSession(self, tstamp):
        pass

    @abc.abstractclassmethod
    def saveHrmData(self, recordSession, hr, rr, sensorContact, tstamp):
        pass

    @abc.abstractclassmethod
    def stopRecordSession(self, tstamp):
        pass


class RecordSession(abc.ABC):
    pass


class HrmHandleNotFoundError(Exception):
    pass


class NoDeviceConnectedError(Exception):
    pass


class ConnectionLostError(Exception):
    pass

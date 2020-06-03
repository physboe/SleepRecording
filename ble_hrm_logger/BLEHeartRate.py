
import logging
import pexpect
import sys
import abc
import time

log = logging.getLogger(__name__)


class RecordingListener(abc.ABC):

    @abc.abstractclassmethod
    def listen(self, hr: int, rr: int, sensorContact: str, tstamp: float):
        pass


class RecordSession(abc.ABC):
    pass


class HrmHandleNotFoundError(Exception):
    pass


class ConnectionLostError(Exception):
    pass


class ConnectionFailed(Exception):

    def __init___(self, deviceMac: str):
        self.deviceMac


class BLEHearRateService:
    # UUID for BLE HearRate Notifier
    HRM_UUID = "00002a37"

    # Names for Result Array
    RESULT_RR_INTERVAL_AVAILABLE = "rr_avb"
    RESULT_RR_INTERVAL = "rr"
    RESULT_HR = "hr"
    RESULT_SENSOR_CONTACT = "sensor_cont"
    RESULT_EE_STATUS = "ee_status"
    RESULT_EE = "ee"
    RESULT_HRV_UINT8 = "hrv_uint8"

    def __init__(self, listener: RecordingListener, debug: bool):
        """
        Parameters
        ----------
        logger : RecordingLoggerInterface
            An implemented object of RecordingLoggerInterface which revices data
        debug : bool
            If you want to debug gatttool output
        """
        self.__listener = listener
        self.__debug = debug
        self.__connected = False

    def connectToDevice(self, deviceMac: str, connectionType: str):
        self.__deviceMac = deviceMac
        log.info("Start gatttool")
        self.__gatttool = self.__startGatttool(deviceMac, connectionType)

        log.info(f"Establishing connection to {deviceMac}")
        self.__connect(self.__gatttool)
        log.info(f"Connected to {deviceMac}")
        self.__connected = True

    def startRecording(self):
        """
        If connected this methode looks for the right hearrate handler and register
        itself.
        It starts to listen and send decodec results to logger

        Parameters
        ----------
        deviceMac : str
            Mac of your Heart Rate BLE device
        connectionType : str
            either random or public depends on your device
        """
        if self.__connected:
            hr_handle, hr_handle_ctl = self.__registeringToHrHandle(self.__gatttool)
            log.info(f"Registered to Handle {hr_handle} on {hr_handle_ctl}")

            log.info(f"Start reading {hr_handle}")
            self.__readOutput(self.__gatttoo, hr_handle)
            log.info(f"Start reading {hr_handle}")

            self.__disconnect(self.__gatttoo)
            log.info(f"Disconnected to {self.__deviceMac}")
        self.__connected = False

    def stopRecording(self):
        if self.__recording:
            self.__recording = False

    def isRecording(self):
        return self.__recording

    def __startGatttool(self, deviceMac: str, connectionType: str):
        gatttool = pexpect.spawn(f"gatttool -b {deviceMac} -t {connectionType} --interactive")
        # enable debug mode in sys out
        if self.__debug:
            gatttool.logfile = sys.stdout.buffer
        return gatttool

    def __disconnect(self, gatttool):
        gatttool.sendline("quit")
        gatttool.wait()

    def __connect(self, gatttool):
        gatttool.expect(r"\[LE\]>")
        gatttool.sendline("connect")
        try:
            i = gatttool.expect(["Connection successful.", r"\[CON\]"], timeout=30)
            if i == 0:
                gatttool.expect(r"\[LE\]>", timeout=30)

        except pexpect.TIMEOUT:
            log.info("Connection timeout.")
            raise ConnectionFailed(self.__deviceMac)

    def __registeringToHrHandle(self, gatttool) -> [str, str]:
        hr_handle, hr_handle_ctl = self.__lookingForHandle(gatttool)
        gatttool.sendline(f"char-write-req {hr_handle_ctl} 0100")
        return hr_handle, hr_handle_ctl

    def __lookingForHandle(self, gatttool)-> [str, str]:
        gatttool.sendline("char-desc")
        while 1:
            try:
                gatttool.expect(r"handle: (0x[0-9a-f]+), uuid: ([0-9a-f]{8})", timeout=10)
            except pexpect.TIMEOUT:
                break

            handle = gatttool.match.group(1).decode()
            uuid = gatttool.match.group(2).decode()

            if uuid == self.HRM_UUID:
                hr_handle = handle
                gatttool.expect(r"handle: (0x[0-9a-f]+), uuid: ([0-9a-f]{8})", timeout=10)
                hr_handle_ctl = gatttool.match.group(1).decode()
                break

        if hr_handle is None:
            log.error("Couldn't find the heart rate measurement handle?!")
            raise HrmHandleNotFoundError(self.HRM_UUID)
        log.debug(f"Found Handle: {hr_handle}")
        return hr_handle, hr_handle_ctl

    def __readOutput(self, gatttool, hr_handle: str):
        self.__recording = True
        notification_expect = f"Notification handle = {hr_handle} value: ([0-9a-f ]+)"
        while self.__recording:
            try:
                gatttool.expect(notification_expect, timeout=10)
                datahex = gatttool.match.group(1).strip()
                data = map(lambda x: int(x, 16), datahex.split(b' '))
                result = self.__interpret(list(data))
            #    self.__sendToDataLogger(result)
                log.debug("Handle Notification: " + str(result))
            except pexpect.TIMEOUT:
                log.warn("Connection lost")
                raise ConnectionLostError("Connection lost")

    def __getTimeStamp(self):
        return int(time.time())

    def __sendToDataLogger(self, result):
        if result[self.RESULT_RR_INTERVAL_AVAILABLE]:
            for rrInterval in result[self.RESULT_RR_INTERVAL]:
                self.__listener.listen(result[self.RESULT_HR], rrInterval, result[self.RESULT_SENSOR_CONTACT], self.__getTimeStamp())
        else:
            self.__listener.listen(result[self.RESULT_HR], rrInterval, result[self.RESULT_SENSOR_CONTACT], self.__getTimeStamp())

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

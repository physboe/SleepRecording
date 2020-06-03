from ble_hrm_logger.BLEHeartRate import BLEHearRateService
from ble_hrm_logger.BLEHeartRate import RecordingListener
import logging
from singleton_decorator import singleton
from threading import Thread
from configs import webapp as config


log = logging.getLogger(__name__)


class HrmListener(RecordingListener):

    def listen(self, hr: int, rr: int, sensorContact: str, tstamp: float):
        log.debug(f"HR: {hr} RR: {rr}")

@singleton
class HrmService():

    CONFIG_DEVICE_MAC = "DEVICE_MAC"
    CONFIG_DEVICE_CONNECTION_TYPE = "DEVICE_CONNECTION_TYPE"
    CONFIG_GATTTOOL_DEBUG = "GATTTOOL_DEBUG"

    def __init__(self):
        log.debug("init")
        self.__blehrs = BLEHearRateService(HrmListener(), config.GATTTOOL_DEBUG)

    def startRecording(self):
        self.__blehrs.connectToDevice(config.DEVICE_MAC, config.DEVICE_CONNECTION_TYPE)
        self.__thread = Thread(target=self.__blehrs.startRecording)
        log.info("start thread")
        self.__thread.start()

    def isRecording(self):
        self.__blehrs.isRecording()

    def stopRecording(self):

        self.__blehrs.stopRecording()
        self.__recordingProcess.join()

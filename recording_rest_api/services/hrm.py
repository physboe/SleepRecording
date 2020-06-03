from ble_hrm_logger.BLEHeartRate import BLEHearRateService
from ble_hrm_logger.BLEHeartRate import RecordingListener
import logging
from singleton_decorator import singleton
from threading import Thread
from recording_rest_api import app


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
        self.__blehrs = BLEHearRateService(HrmListener(), app.config[self.CONFIG_GATTTOOL_DEBUG])

    def startRecording(self):
        mac = app.config[self.CONFIG_DEVICE_MAC]
        type = app.config[self.CONFIG_DEVICE_CONNECTION_TYPE]
        self.__thread = Thread(target=self.__blehrs.startRecording, args=(mac, type))
        log.info("start thread")
        self.__thread .start()

    def isRecording(self):
        self.__blehrs.isRecording()

    def stopRecording(self):

        self.__blehrs.stopRecording()
        self.__recordingProcess.join()

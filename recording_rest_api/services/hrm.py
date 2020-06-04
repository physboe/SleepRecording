from ble_hrm_logger.BLEHeartRate import BLEHearRateService, RecordingListener
from recording_rest_api.services.manager import RecordingService
from singleton_decorator import singleton
from threading import Thread
from configs import webapp as config
import logging


log = logging.getLogger(__name__)


class HrmListener(RecordingListener):

    def listen(self, hr: int, rr: int, sensorContact: str, tstamp: float):
        log.debug(f"HR: {hr} RR: {rr}")


@singleton
class HrmService(RecordingService):

    def __init__(self):
        log.debug("init")
        self.__blehrs = BLEHearRateService(HrmListener(), config.GATTTOOL_DEBUG)

    def startRecording(self):
        if not self.__blehrs.isRecording():
            self.__blehrs.connectToDevice(config.DEVICE_MAC, config.DEVICE_CONNECTION_TYPE)
            self.__thread = Thread(target=self.__blehrs.startRecording)
            log.info("Start thread")
            self.__thread.start()

    def isRecording(self) -> bool:
        log.info(self.__blehrs.isRecording())
        return self.__blehrs.isRecording()

    def stopRecording(self):
        if self.__blehrs.isRecording():
            self.__blehrs.stopRecording()
            self.__thread.join()

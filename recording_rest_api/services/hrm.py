from ble_hrm_logger.BLEHeartRate import BLEHearRateService, RecordingListener
from recording_rest_api.services import RecordingService
from recording_rest_api.database.recording import DaoRecordSession
from singleton_decorator import singleton
from threading import Thread
from configs import webapp as config
import logging


log = logging.getLogger(__name__)


class HrmListener(RecordingListener):

    def __init__(self, recordSession: DaoRecordSession):
        self.__recordSession = recordSession

    def listen(self, hr: int, rr: int, sensorContact: str, tstamp: float):
            log.debug(f"HR: {hr} RR: {rr}")
            pass


class HrmService(RecordingService):

    def __init__(self):
        log.debug("init")
        self.__blehrs = BLEHearRateService(config.GATTTOOL_DEBUG)

    def startRecording(self, recordSession: DaoRecordSession):
        if not self.__blehrs.isRecording():
            self.__blehrs.connectToDevice(config.DEVICE_MAC, config.DEVICE_CONNECTION_TYPE)
            self.__thread = Thread(target=self.__blehrs.startRecording, args=(HrmListener(recordSession),))
            log.info("Start thread")
            self.__thread.start()

    def isRecording(self) -> bool:
        log.info(self.__blehrs.isRecording())
        return self.__blehrs.isRecording()

    def stopRecording(self):
        if self.__blehrs.isRecording():
            self.__blehrs.stopRecording()
            self.__thread.join()

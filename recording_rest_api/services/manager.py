from singleton_decorator import singleton
from recording_rest_api.services.hrm import HrmService
import logging


log = logging.getLogger(__name__)


@singleton
class RecordingManager():

    def __init__(self):
        """
        Init all services
        """
        log.info("Init ServicesManager")
        self.__services = [HrmService()]
        self.__recoding = False

    def startRecordings(self):
        log.info("Starting Services")
        # Insert DB
        for service in self.__services:
            service.startRecording()
        self.__recording = True
        log.info("Services started")

    def stopRecordings(self):
        log.info("Stopping Services")
        # Update DB
        for service in self.__services:
            service.stopRecording()
        self.__recoding = False
        log.info("Services stopped")

    def isRecording(self) -> bool:
        return self.__recoding

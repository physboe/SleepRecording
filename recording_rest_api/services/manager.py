from singleton_decorator import singleton
from recording_rest_api.services.hrm import HrmService
import logging
import abc


log = logging.getLogger(__name__)

class RecordingService(abc.ABC):

    @abc.abstractclassmethod
    def startRecording(self):
        pass

    @abc.abstractclassmethod
    def isRecording(self) -> bool:
        pass

    @abc.abstractclassmethod
    def stopRecording(self):
        pass


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
        log.info("Starting Services")
        # Update DB
        for service in self.__services:
            service.stopRecording()
        self.__recoding = False
        log.info("Services started")

    def isRecording(self) -> bool:
        return self.__recoding

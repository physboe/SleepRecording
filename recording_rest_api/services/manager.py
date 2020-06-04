from singleton_decorator import singleton
from recording_rest_api.services.hrm import HrmService
from recording_rest_api.database.recording import DaoRecordSession
from recording_rest_api.database import db
import time
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
        self.__recording = False

    def startRecordings(self, tag: str):
        log.info("Starting Services")
        self.__recordsession = self.__createRecordSession(tag)
        for service in self.__services:
            service.startRecording(self.__recordsession, tag)
        self.__recording = True
        log.info("Services started")

    def stopRecordings(self):
        log.info("Stopping Services")

        for service in self.__services:
            service.stopRecording()

        self.__recording = False

        log.info("Services stopped")

    def isRecording(self) -> bool:
        return self.__recording

    def __createRecordSession(self, tag: str) -> DaoRecordSession:
        recordsession = DaoRecordSession(time.time(), tag)
        db.session.add(recordsession)
        return recordsession

    def __updateRecordSession(self, recordsession: DaoRecordSession, tag: str):
        db.session.add(recordsession)
        db.session.commit()

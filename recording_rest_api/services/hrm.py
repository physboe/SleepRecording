from ble_hrm_logger import BLEHeartRate as ble
from ble_hrm_logger import DatabaseLayer as dbl
import configparser
import os
import logging
from singleton_decorator import singleton
from multiprocessing import Process

log = logging.getLogger(__name__)

@singleton
class HrmService():

    def __init__(self):
        log.debug("init")
        self.__loadConfig()
        self.__blehrs = ble.BLEHearRateService(self.__configs['config']['debug'])
        self.__db = dbl.DatabaseService(self.__configs['config']['output'])

    def startRecording(self):
        self.__blehrs.connectToDevice(self.__configs['config']['mac'], self.__configs['config']['type'])
        self.__blehrs.registeringToHrHandle()
        self.__recordingProcess = Process(target=self.__blehrs.startRecording, args=(self.__db,))
        self.__recordingProcess.start()

    def isRecording(self):
        self.__blehrs.isRecording()

    def stopRecording(self):

        self.__blehrs.stopRecording()
        self.__recordingProcess.join()
        self.__blehrs.close()
        self.recording = False

    def __loadConfig(self):
        confpath = os.path.join("configs", "SuuntoLocal.conf")
        config = configparser.ConfigParser()
        config.read(confpath)
        self.__configs = config
        log.debug(self.__configs)

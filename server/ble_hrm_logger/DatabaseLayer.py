import sqlite3
from ble_hrm_logger import BLEHeartRate as bleservice
import logging

log = logging.getLogger(__name__)


class DatabaseService(bleservice.RecordingListener):

    COMMIT_COUNT = 15
    SQL_CREATE_RECORDSESSION = "CREATE TABLE IF NOT EXISTS recordsession (recordsession_id INTEGER PRIMARY KEY AUTOINCREMENT, start INTEGER, end INTEGER)"
    SQL_CREATE_HRM_DATA = "CREATE TABLE IF NOT EXISTS hrm (tstamp INTEGER, hr INTEGER, rr INTEGER, sensor_contact TEXT , fk_recordsession_id INTEGER, FOREIGN KEY(fk_recordsession_id) REFERENCES recordsession(recordsession_id))"
    SQL_INSERT_RECORDSESSION = "INSERT INTO recordsession (start) VALUES (?)"
    SQL_UPDATE_RECORDSESSION = "UPDATE recordsession SET end = ? where recordsession_id = ?"
    SQL_INSERT_HRM_DATA = "INSERT INTO hrm (tstamp, hr, rr, sensor_contact, fk_recordsession_id) VALUES (?, ?, ?, ?, ?)"

    def __init__(self, databaseurl: str):
        self.__databaseurl = databaseurl
        db = self.__connectToDb()
        db.execute(self.SQL_CREATE_RECORDSESSION)
        db.execute(self.SQL_CREATE_HRM_DATA)
        self.__recordSession = None
        self.__db = db

    def __updateRecordSession(self, recordsession_id, tstamp):
        cru = self.__db.execute(self.SQL_UPDATE_RECORDSESSION, (tstamp,recordsession_id))
        self.__db.commit()
        return cru.lastrowid

    def __insertRecordSession(self, tstamp):
        cru = self.__db.execute(self.SQL_INSERT_RECORDSESSION, (tstamp,))
        self.__db.commit()
        return cru.lastrowid

    def ___insertHrmData(self, recordsession_id: int, hr: int, rr, sensor_contact, tstamp):
        self.__db.execute(self.SQL_INSERT_HRM_DATA, (tstamp, hr, rr, sensor_contact, recordsession_id))
        self.__counter = self.__counter + 1
        if self.__counter >= self.COMMIT_COUNT:
            log.debug("Commit hrm_data")
            self.__db.commit()
            self.__counter = 0

    def __connectToDb(self):
        db = sqlite3.connect(self.__databaseurl)
        log.info("Connected to database")
        return db

    def __closeDB(self, db):
        db.commit()
        db.close()
        log.info("Database closed")

    def startRecordSession(self, tstamp: float):
        self.__db = self.__connectToDb()
        self.__counter = 0
        self.__recordSession = DaoRecordSession(self.__insertRecordSession(tstamp))

    def listen(self, hr: int, rr: int, sensorContact: str, tstamp: float):
        self.___insertHrmData(self.__recordSession.getId(), hr, rr, sensorContact, tstamp)

    def stopRecordSession(self, tstamp: float):
        self.__updateRecordSession(self.__recordSession.getId(), tstamp)
        self.__counter = 0
        self.__closeDB(self.__db)
        self.__db = None


class DaoRecordSession(bleservice.RecordSession):

    def __init__(self, id):
        self.__id = id

    def getId(self):
        return self.__id

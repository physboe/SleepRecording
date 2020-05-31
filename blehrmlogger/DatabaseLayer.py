import sqlite3
from blehrmlogger import BLEHeartRateService as bleservice
import logging


class DatabaseLayer(bleservice.RecordingLoggerInterface):

    def __init__(self, databaseurl):
        self.__databaseurl = databaseurl
        db = self.__connectToDb()
        db.execute("CREATE TABLE IF NOT EXISTS recordsession (recordsession_id INTEGER PRIMARY KEY AUTOINCREMENT, start INTEGER, end INTEGER)")
        db.execute("CREATE TABLE IF NOT EXISTS hrm (tstamp INTEGER, hr INTEGER, rr INTEGER, sensor_context TEXT , fk_recordsession_id INTEGER, FOREIGN KEY(fk_recordsession_id) REFERENCES recordsession(recordsession_id))")
        self.__closeDB(db)

    def __updateRecordSession(self, recordsession_id, tstamp):
        cru = self.db.execute("UPDATE recordsession SET end = ? where recordsession_id = ?", (tstamp,recordsession_id))
        self.db.commit()
        return cru.lastrowid

    def __insertRecordSession(self, tstamp):
        cru = self.db.execute("INSERT INTO recordsession (start) VALUES (?)", (tstamp,))
        self.db.commit()
        return cru.lastrowid

    def ___insertHrmData(self, recordsession_id, hr, rr, tstamp):
        self.db.execute("INSERT INTO hrm (tstamp, hr, rr, fk_recordsession_id) VALUES (?, ?, ?, ?)", (tstamp, hr, rr, recordsession_id))
        self.counter = self.counter + 1
        if self.counter >= 5:
            logging.info("Commit hrm_data")
            self.db.commit()
            self.counter = 0

    def __connectToDb(self):
        db = sqlite3.connect(self.__databaseurl)
        logging.info("Connected to database")
        return db

    def __closeDB(self, db):
        db.commit()
        db.close()
        logging.info("Database closed")

    def startRecordSession(self, tstamp):
        self.db = self.__connectToDb()
        self.counter = 0
        return DaoRecordSession(self.__insertRecordSession(tstamp))

    def saveHrmData(self, recordSession, hr, rr, tstamp):
        self.___insertHrmData(recordSession.getId(), hr, rr, tstamp)

    def stopRecordSession(self, recordSession, tstamp):
        self.__updateRecordSession(recordSession.getId(), tstamp)
        self.counter = 0
        self.db.commit()
        self.db.close()
        self.db = None


class DaoRecordSession(bleservice.RecordSession):

    def __init__(self, id):
        self.__id = id

    def getId(self):
        return self.__id

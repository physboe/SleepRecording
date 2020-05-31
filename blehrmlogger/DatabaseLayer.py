import sqlite3
import time
from ble_rr_logger import RecordingLoggerInterface as ri
import logging


class DatabaseLayer(ri.RecordingLoggerInterface):

    def __init__(self, databaseurl):
        self.db = sqlite3.connect(databaseurl)
        self.db.execute("CREATE TABLE IF NOT EXISTS recordsession (recordsession_id INTEGER PRIMARY KEY AUTOINCREMENT, tstamp INTEGER)")
        self.db.execute("CREATE TABLE IF NOT EXISTS hrm (tstamp INTEGER, hr INTEGER, rr INTEGER, fk_recordsession_id INTEGER, FOREIGN KEY(fk_recordsession_id) REFERENCES recordsession(recordsession_id))")
        self.db.execute("CREATE TABLE IF NOT EXISTS sql (tstamp INTEGER, commit_time REAL, commit_every INTEGER)")
        self.counter = 0
        logging.info("Database created")

    def __insertRecordSession(self, tstamp):
        cru = self.db.execute("INSERT INTO recordsession (tstamp) VALUES (?)", (tstamp,))
        self.db.commit()
        return cru.lastrowid

    def ___insertHrmData(self, recordsession_id, hr, rr, tstamp):
        self.db.execute("INSERT INTO hrm (tstamp, hr, rr, fk_recordsession_id) VALUES (?, ?, ?, ?)", (tstamp, hr, rr, recordsession_id))
        self.counter = self.counter + 1
        if self.counter >= 5:
            self.db.commit()
            self.counter = 0

    def saveRecordSession(self, tstamp):
        return DaoRecordSession(self.__insertRecordSession(tstamp))

    def saveHrmData(self, recordSession, hr, rr, tstamp):
        self.___insertHrmData(recordSession.getId(), hr, rr, tstamp)

    def close(self):
        self.db.commit()
        self.db.close()
        logging.info("Database closed")


class DaoRecordSession(ri.RecordSession):

    def __init__(self, id):
        self.__id = id

    def getId(self):
        return self.__id

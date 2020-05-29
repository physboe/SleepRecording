import sqlite3
import time


class DatabaseLayer:

    def __init__(self, databaseurl):
        self.db = sqlite3.connect(databaseurl)
        self.db.execute("CREATE TABLE IF NOT EXISTS recordsession (recordsession_id INTEGER PRIMARY KEY AUTOINCREMENT, tstamp INTEGER)")
        self.db.execute("CREATE TABLE IF NOT EXISTS hrm (tstamp INTEGER, hr INTEGER, rr INTEGER, fk_recordsession_id INTEGER, FOREIGN KEY(fk_recordsession_id) REFERENCES recordsession(recordsession_id))")
        self.db.execute("CREATE TABLE IF NOT EXISTS sql (tstamp INTEGER, commit_time REAL, commit_every INTEGER)")
        self.counter = 0

    def insertRecordSession(self):
        cru = self.db.execute("INSERT INTO recordsession (tstamp) VALUES (?)", (self._getTimestamp(),))
        self.db.commit()
        return cru.lastrowid

    def _getTimestamp(self):
        return int(time.time())

    def insertHrmData(self, recordsession_id, hr, rr):
        self.db.execute("INSERT INTO hrm (tstamp, hr, rr, fk_recordsession_id) VALUES (?, ?, ?, ?)", (self._getTimestamp(), hr, rr, recordsession_id))
        self.counter = self.counter + 1
        if self.counter >= 5:
            self.db.commit()
            self.counter = 0

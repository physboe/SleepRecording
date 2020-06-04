from ble_hrm_logger import DatabaseLayer as dbl
import unittest
import sqlite3
import time
import logging


class TestDatabaseLayer(unittest.TestCase):

    def test_init(self):
        try:
            dbl.DatabaseService("test.db")
        except Exception as e:
            self.fail(e.message)

    def test_insert_recordsession(self):
            try:
                db = dbl.DatabaseService("test.db")
                recordSession = db.startRecordSession(self.__getTimestamp())
                db.stopRecordSession(recordSession, self.__getTimestamp())
                db = sqlite3.connect("test.db")
                laenge = len(
                            db.execute(
                            "SELECT * from recordsession where recordsession_id = "
                            + str(recordSession.getId())).fetchall())
                self.assertEqual(laenge, 1)
            except Exception as e:
                self.fail(e)
                logging.exception(e, exc_info=True)

    def test_insert_five_recordsession(self):
            try:
                db = dbl.DatabaseService("test.db")
                id = db.startRecordSession(self.__getTimestamp())
                db.saveHrmData(id, 85, 722, 'lose', self.__getTimestamp())
                db.saveHrmData(id, 85, 722, 'lose', self.__getTimestamp())
                db.saveHrmData(id, 85, 722, 'lose', self.__getTimestamp())
                db.saveHrmData(id, 85, 722, 'lose', self.__getTimestamp())
                db.saveHrmData(id, 85, 722, 'lose', self.__getTimestamp())
                db.stopRecordSession(id, self.__getTimestamp())

                db = sqlite3.connect("test.db")
                self.assertEqual(len(db.execute("SELECT * from hrm where hrm.fk_recordsession_id=" + str(id.getId())).fetchall()), 5)
            except Exception as e:
                self.fail(e)
                logging.exception(e, exc_info=True)

    def test_insert_six_recordsession(self):
            try:
                db = dbl.DatabaseService("test.db")
                id = db.startRecordSession(self.__getTimestamp())
                db.saveHrmData(id, 85, 722, 'lose', self.__getTimestamp())
                db.saveHrmData(id, 85, 722, 'lose', self.__getTimestamp())
                db.saveHrmData(id, 85, 722, 'lose', self.__getTimestamp())
                db.saveHrmData(id, 85, 722, 'lose', self.__getTimestamp())
                db.saveHrmData(id, 85, 722, 'lose', self.__getTimestamp())
                db.saveHrmData(id, 85, 722, 'lose', self.__getTimestamp())
                db.stopRecordSession(id, self.__getTimestamp())

                db = sqlite3.connect("test.db")
                self.assertEqual(len(db.execute("SELECT * from hrm where hrm.fk_recordsession_id=" + str(id.getId())).fetchall()), 6)
            except Exception as e:
                self.fail(e)
                logging.exception(e, exc_info=True)

    def test_insert_two_recordsession(self):
            try:
                db = dbl.DatabaseService("test.db")
                id = db.startRecordSession(self.__getTimestamp())
                db.saveHrmData(id, 85, 722, 'lose', self.__getTimestamp())
                db.saveHrmData(id, 85, 722, 'lose', self.__getTimestamp())
                db.stopRecordSession(id, self.__getTimestamp())

                db = sqlite3.connect("test.db")
                self.assertEqual(len(db.execute("SELECT * from hrm where hrm.fk_recordsession_id=" + str(id.getId())).fetchall()), 2)
            except Exception as e:
                self.fail(e)
                logging.exception(e, exc_info=True)

    def __getTimestamp(self):
            return int(time.time())

import ble_rr_Logger.DatabaseLayer as dbl
import unittest
import sqlite3


class TestDatabaseLayer(unittest.TestCase):

    def test_init(self):
        try:
            dbl.DatabaseLayer("test.db")
        except Exception as e:
            self.fail(e.message)

    def test_insert_recordsession(self):
            try:
                db = dbl.DatabaseLayer("test.db")
                db.insertRecordSession()
                db = sqlite3.connect("test.db")
                self.assertEqual(len(db.execute("SELECT * from recordsession").fetchall()),1 )
            except Exception as e:
                self.fail(e.message)


    def test_insert_recordsession(self):
            try:
                db = dbl.DatabaseLayer("test.db")
                id = db.insertRecordSession()
                db.insertHrmData(id, 85, 722)
                db.insertHrmData(id, 85, 722)
                db.insertHrmData(id, 85, 722)
                db.insertHrmData(id, 85, 722)
                db.insertHrmData(id, 85, 722)
                db.insertHrmData(id, 85, 722)
                db = sqlite3.connect("test.db")
                self.assertEqual(len(db.execute("SELECT * from hrm").fetchall()), 5 )
            except Exception as e:
                self.fail(e.message)

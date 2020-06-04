from recording_rest_api.database import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class DaoRecordSession(db.Model):
    __tablename__ = 'recordsession'

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.Float)
    stopTime = db.Column(db.Float)
    sqlite_autoincrement=True
    
    def __init__(self, startTime: float):
        self.startTime = startTime

    def __repr__(self):
        return f'<DaoRecordSession id:{self.id}, startTime: {self.startTime}, stopTime: {self.stopTime}>'


class DaoHrmRecord(db.Model):
    __tablename__ = 'hrmrecord'

    id = db.Column(db.Integer, primary_key=True)
    hr = db.Column(db.Integer)
    rr = db.Column(db.Integer)
    sensorContact = db.Column(db.Text)
    time = db.Column(db.Float)
    recordsessionId = (db.Integer, ForeignKey('recordsession.id'))
    sqlite_autoincrement=True

    recordSession = relationship("recordsession")

    def __init__(self, hr: int, rr: int, sensorContact: str, time: float, recordSession: DaoRecordSession):
        self.hr = hr
        self.rr = rr
        self.sensorContact = sensorContact
        self.time = time
        self.recordSession = recordSession

    def __repr__(self):
        return f'<DaoHrmRecord id:{self.id}, hr: {self.hr}, rr: {self.rr}, sensorConact: {self.sensorContact}, >'


class RecordingState():
    running: bool

    def __init__(self, running: bool):
        self.running = running

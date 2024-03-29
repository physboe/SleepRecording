from recording_rest_api.database import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class DaoRecordSession(db.Model):
    __tablename__ = 'recordsession'
  #  __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.Float)
    stopTime = db.Column(db.Float)
    tag = db.Column(db.Text)
    hrmrecords = relationship("DaoHrmRecord", back_populates="recordSession")

    def __init__(self, startTime: float, tag: str):
        self.startTime = startTime
        self.tag = tag

    def __repr__(self):
        return f'<DaoRecordSession id:{self.id}, startTime: {self.startTime}, stopTime: {self.stopTime}>'


class DaoHrmRecord(db.Model):
    __tablename__ = 'hrmrecord'
 #
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    hr = db.Column(db.Integer)
    rr = db.Column(db.Integer)
    sensorContact = db.Column(db.Text)
    time = db.Column(db.Float)
    recordsessionId = db.Column(db.Integer, ForeignKey('recordsession.id'))

    recordSession = relationship("DaoRecordSession", back_populates="hrmrecords")

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
    tag: str

    def __init__(self, running: bool):
        self.running = running

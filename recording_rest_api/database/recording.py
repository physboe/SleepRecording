from recording_rest_api.database import db


class DaoRecordSession(db.Model):
    __tablename__ = 'recordsession'

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.Float)
    stopTime = db.Column(db.Float)

    def __init__(self, startTime: float):
        self.startTime = startTime

    def __repr__(self):
        return f'<DaoRecordSession id:{self.id}, startTime: {self.startTime}, stopTime: {self.stopTime}>'


class RecordingState():
    running: bool

    def __init__(self, running: bool):
        self.running = running

import abc
from recording_rest_api.database.recording import DaoRecordSession

class RecordingService(abc.ABC):

    @abc.abstractclassmethod
    def startRecording(self, record: DaoRecordSession):
        pass

    @abc.abstractclassmethod
    def isRecording(self) -> bool:
        pass

    @abc.abstractclassmethod
    def stopRecording(self):
        pass

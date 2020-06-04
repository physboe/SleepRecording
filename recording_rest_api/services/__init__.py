import abc

class RecordingService(abc.ABC):

    @abc.abstractclassmethod
    def startRecording(self):
        pass

    @abc.abstractclassmethod
    def isRecording(self) -> bool:
        pass

    @abc.abstractclassmethod
    def stopRecording(self):
        pass

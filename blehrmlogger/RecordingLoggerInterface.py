#import abc


class RecordingLoggerInterface():

#    @abc.abstractclassmethod
    def __init__(self):
        pass

    #@abc.abstractclassmethod
    def saveRecordSession(self, tstamp):
        pass

#    @abc.abstractclassmethod
    def saveHrmData(self, recordSession, hr, rr, tstamp):
        pass

    #@abc.abstractclassmethod
    def close(self):
        pass


class RecordSession():

    def __init__(self):
        pass

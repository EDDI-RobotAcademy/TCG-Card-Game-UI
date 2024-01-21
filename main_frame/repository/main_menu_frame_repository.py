import abc


class MainMenuFrameRepository(abc.ABC):

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def createMainMenuFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def requestProgramExit(self, programExitRequest):
        pass



    
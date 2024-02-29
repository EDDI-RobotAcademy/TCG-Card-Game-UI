import abc


class RockPaperScissorsRepository(abc.ABC):
    @abc.abstractmethod
    def createRockPaperScissorsFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def setRPS(self, rps):
        pass

    @abc.abstractmethod
    def getRPS(self):
        pass

    @abc.abstractmethod
    def requestRockPaperscissors(self, RockPaperScissorsRequest):
        pass
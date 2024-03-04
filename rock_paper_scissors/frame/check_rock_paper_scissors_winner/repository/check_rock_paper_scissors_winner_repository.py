import abc


class CheckRockPaperScissorsWinnerRepository(abc.ABC):
    @abc.abstractmethod
    def createCheckRockPaperScissorsWinnerFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def requestCheckRockPaperScissorsWinner(self, CheckRockPaperScissorsWinnerRequest):
        pass

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def setRPSWinner(self, RPSWinner):
        pass

    @abc.abstractmethod
    def getRPSWinner(self):
        pass

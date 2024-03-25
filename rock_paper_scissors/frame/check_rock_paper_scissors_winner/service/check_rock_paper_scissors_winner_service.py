import abc


class CheckRockPaperScissorsWinnerService(abc.ABC):
    @abc.abstractmethod
    def createCheckRockPaperScissorsWinnerUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def injectReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def findWinner(self):
        pass

    @abc.abstractmethod
    def check_RPSWinner(self, rootWindow, switchFrameWithMenuName):
        pass


import abc


class RockPaperScissorsService(abc.ABC):
    @abc.abstractmethod
    def createRockPaperScissorsUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass

    @abc.abstractmethod
    def findRPS(self):
        pass

    @abc.abstractmethod
    def startRPS_Timer(self):
        pass

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def injectReceiveIpcChannel(self, receiveIpcChannel):
        pass


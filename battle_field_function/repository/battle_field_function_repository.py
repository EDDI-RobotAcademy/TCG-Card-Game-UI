import abc


class BattleFieldFunctionRepository(abc.ABC):

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def sendSurrender(self, surrenderRequest):
        pass
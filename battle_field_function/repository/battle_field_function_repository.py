import abc


class BattleFieldFunctionRepository(abc.ABC):

    @abc.abstractmethod
    def saveRoomNumber(self, roomNumber):
        pass

    @abc.abstractmethod
    def getRoomNumber(self):
        pass

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def requestSurrender(self, surrenderRequest):
        pass

    @abc.abstractmethod
    def requestTurnEnd(self, turnEndRequest):
        pass




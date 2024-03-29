import abc


class BattleFieldFunctionService(abc.ABC):

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def injectReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def surrender(self, switchFrameWithMenuName):
        pass



    @abc.abstractmethod
    def turnEnd(self):
        pass


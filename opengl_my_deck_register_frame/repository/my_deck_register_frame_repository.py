import abc

class MyDeckRegisterFrameRepository(abc.ABC):

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def requestRegister(self, myDeckRegisterRequest):
        pass
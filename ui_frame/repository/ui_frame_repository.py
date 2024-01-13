import abc


class UiFrameRepository(abc.ABC):

    @abc.abstractmethod
    def switchFrameWithMenuName(self, menu_name):
        pass

    @abc.abstractmethod
    def registerUiFrame(self, name, newFrame):
        pass

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass


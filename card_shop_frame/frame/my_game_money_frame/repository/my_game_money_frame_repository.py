import abc


class MyGameMoneyFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createMyGameMoneyFrame(self, rootWindow):
        pass

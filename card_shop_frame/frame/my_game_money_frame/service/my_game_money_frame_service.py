import abc


class MyGameMoneyFrameService(abc.ABC):
    @abc.abstractmethod
    def createMyGameMoneyUiFrame(self, rootWindow):
        pass
    @abc.abstractmethod
    def findMyMoney(self):
        pass

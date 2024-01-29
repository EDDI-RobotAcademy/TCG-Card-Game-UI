import abc


class MyCardMainFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createMyCardMainFrame(self, rootWindow):
        pass
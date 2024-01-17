import abc


class MakeMyDeckFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createMakeMyDeckFrame(self, rootWindow):
        pass
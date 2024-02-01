import abc


class MatchingWindowController(abc.ABC):


    @abc.abstractmethod
    def makeMatchingWindow(self, rootWindow):
        pass

    @abc.abstractmethod
    def matching(self, rootWindow):
        pass
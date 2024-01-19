import abc


class TransparentBackgroundFrameRepository(abc.ABC):

    @abc.abstractmethod
    def Create_rectangle(self, frame, x1, y1, x2, y2, **kwargs):
        pass
    @abc.abstractmethod
    def createTransparentBackgroundFrame(self, rootWindow):
        pass
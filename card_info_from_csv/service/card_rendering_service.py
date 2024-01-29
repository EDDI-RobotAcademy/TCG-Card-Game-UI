import abc


class CardRenderingService(abc.ABC):

    @abc.abstractmethod
    def registerCardRenderingInfo(self, cardNumber):
        pass
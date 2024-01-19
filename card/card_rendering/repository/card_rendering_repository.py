import abc


class CardRenderingRepository(abc.ABC):

    @abc.abstractmethod
    def registerCardInfo(self, cardNumber):
        pass
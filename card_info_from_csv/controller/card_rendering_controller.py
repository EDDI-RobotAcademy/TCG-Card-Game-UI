import abc

class CardRenderingController(abc.ABC):

    @abc.abstractmethod
    def requestToCardRenderingCardNumber(self, cardNumber):
        pass

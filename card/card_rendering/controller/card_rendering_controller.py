import abc

class CardRenderingController(abc.ABC):

    @abc.abstractmethod
    def cardRender(self, cardNumber, cardSize):
        pass

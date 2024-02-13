import abc

class ButtonHandler(abc.ABC):

    @abc.abstractmethod
    def myDeckRegisterScreen(self, master, frame):
        pass

    # @abc.abstractmethod
    # def goToLobbyFrame(self, master, frame):
    #     pass
    #
    # @abc.abstractmethod
    # def createDeck(self, master, frame):
    #     pass
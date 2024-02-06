import abc

class ButtonHandler(abc.ABC):

    @abc.abstractmethod
    def myDeckRegisterScreen(self, master, canvas, scene):
        pass

    @abc.abstractmethod
    def goToLobbyFrame(self):
        pass
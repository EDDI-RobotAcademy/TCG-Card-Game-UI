import abc


class MusicPlayerController(abc.ABC):
    @abc.abstractmethod
    def loadAllMusicFiles(self):
        pass

    @abc.abstractmethod
    def playBackgroundMusic(self):
        pass

    @abc.abstractmethod
    def requestToInjectUiIpcChannel(self, uiIpcChannel):
        pass

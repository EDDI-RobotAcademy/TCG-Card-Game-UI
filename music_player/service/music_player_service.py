import abc


class MusicPlayerService(abc.ABC):
    @abc.abstractmethod
    def loadBackgroundMusics(self):
        pass

    @abc.abstractmethod
    def loadSoundEffects(self):
        pass

    @abc.abstractmethod
    def playBackgroundMusic(self):
        pass

    @abc.abstractmethod
    def injectUiIpcChannel(self, uiIpcChannel):
        pass

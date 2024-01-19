import abc


class MusicPlayerRepository(abc.ABC):
    @abc.abstractmethod
    def loadBackgroundMp3(self, frameName: str):
        pass

    @abc.abstractmethod
    def playBackgroundMusic(self):
        pass

    @abc.abstractmethod
    def getBackgroundMusicFilePath(self):
        pass

    @abc.abstractmethod
    def saveUiIpcChannel(self, uiIpcChannel):
        pass

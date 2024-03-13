import abc


class MusicPlayerRepository(abc.ABC):
    @abc.abstractmethod
    def loadBackgroundMusic(self, frameName: str):
        pass

    @abc.abstractmethod
    def playBackgroundMusic(self):
        pass

    # @abc.abstractmethod
    # def changeBackgroundMusic(self):
    #     pass
    #
    # @abc.abstractmethod
    # def getBackgroundMusicFilePath(self, frameName):
    #     pass
    #
    # @abc.abstractmethod
    # def detectFrameChange(self):
    #     pass

    @abc.abstractmethod
    def saveUiIpcChannel(self, uiIpcChannel):
        pass

import abc


class MusicPlayerService(abc.ABC):
    @abc.abstractmethod
    def playMusicWithFrameName(self, frameName):
        pass

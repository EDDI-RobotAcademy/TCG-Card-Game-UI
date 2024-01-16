import abc


class MusicPlayerRepository(abc.ABC):
    @abc.abstractmethod
    def playMusicWithFrameName(self, frameName):
        pass

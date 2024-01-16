from pygame import mixer
from music_player.repository.music_player_repository import MusicPlayerRepository


class MusicPlayerRepositoryImpl(MusicPlayerRepository):
    __instance = None
    __music_file = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        mixer.init()

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def playMusicWithFrameName(self, frameName):
        self.__music_file = f"/home/eddi/proj/TCG-Card-Game-UI/tests/music_player/music/{frameName}.mp3"

        mixer.music.load(self.__music_file)
        mixer.music.play()

import os
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
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.__music_file = os.path.join(script_dir, "../../", "local_storage", "music", f"{frameName}.mp3")
        mixer.music.load(self.__music_file)
        mixer.music.play()

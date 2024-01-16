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

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def playMusicWithFrameName(self, frameName):
        mixer.init()
        print(mixer)
        script_dir = os.getcwd()
        print(script_dir)
        self.__music_file = os.path.join(script_dir, "../../", "local_storage", "music", f"{frameName}.mp3")
        print(self.__music_file)
        mixer.music.load(self.__music_file)
        mixer.music.play()

        if mixer.music.get_busy():
            print("Music is playing")

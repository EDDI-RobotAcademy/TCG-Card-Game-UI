import os
from music_player.repository.music_player_repository_impl import MusicPlayerRepositoryImpl
from music_player.service.music_player_service import MusicPlayerService


class MusicPlayerServiceImpl(MusicPlayerService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__musicPlayerRepository = MusicPlayerRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def loadBackgroundMusics(self):
        self.__musicPlayerRepository.loadBackgroundMusicPath("main-menu")
        self.__musicPlayerRepository.loadBackgroundMusicPath("lobby-menu")
        self.__musicPlayerRepository.loadBackgroundMusicPath("battle-lobby")
        self.__musicPlayerRepository.loadBackgroundMusicPath("my-card-main")
        self.__musicPlayerRepository.loadBackgroundMusicPath("card-shop-menu")

    def playBackgroundMusic(self):
        print("MusicPlayerServiceImpl : playBackgroundMusic")
        # self.__musicPlayerRepository.detectFrameChange()
        self.__musicPlayerRepository.playBackgroundMusic()

    def injectUiIpcChannel(self, uiIpcChannel):
        self.__musicPlayerRepository.saveUiIpcChannel(uiIpcChannel)

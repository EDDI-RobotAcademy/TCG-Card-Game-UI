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
        self.__musicPlayerRepository.loadBackgroundMp3("main-menu")

    def playBackgroundMusic(self):
        self.__musicPlayerRepository.playBackgroundMusic()

    def injectUiIpcChannel(self, uiIpcChannel):
        self.__musicPlayerRepository.saveUiIpcChannel(uiIpcChannel)

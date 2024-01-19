from music_player.controller.music_player_controller import MusicPlayerController
from music_player.service.music_player_service_impl import MusicPlayerServiceImpl


class MusicPlayerControllerImpl(MusicPlayerController):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__musicPlayerService = MusicPlayerServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def loadAllMusicFiles(self):
        print("MusicPlayerController - loadAllMusicFiles")
        self.__musicPlayerService.loadBackgroundMusics()
        # self.__musicPlayerService.loadEffectSounds()

    def playBackgroundMusic(self):
        print("MusicPlayerController - playMusic")
        self.__musicPlayerService.playBackgroundMusic()

    def requestToInjectUiIpcChannel(self, uiIpcChannel):
        print("MusicPlayerController - requestToInjectUiIpcChannel")
        self.__musicPlayerService.injectUiIpcChannel(uiIpcChannel)

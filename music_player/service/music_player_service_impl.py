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
        print("MusicPlayerServiceImpl : loadBackgroundMusics")
        self.__musicPlayerRepository.load_background_music_path_with_frame_name("main-menu")
        self.__musicPlayerRepository.load_background_music_path_with_frame_name("lobby-menu")
        self.__musicPlayerRepository.load_background_music_path_with_frame_name("battle-lobby")
        self.__musicPlayerRepository.load_background_music_path_with_frame_name("my-card-main")
        self.__musicPlayerRepository.load_background_music_path_with_frame_name("card-shop-menu")
        self.__musicPlayerRepository.load_background_music_path_with_frame_name("fake-battle-field")
        self.__musicPlayerRepository.load_background_music_path_with_frame_name("battle-field")

    def loadSoundEffects(self):
        self.__musicPlayerRepository.load_sound_effect_path_with_event_name("basic_attack")

    def playBackgroundMusic(self):
        print("MusicPlayerServiceImpl : playBackgroundMusic")
        self.__musicPlayerRepository.play_background_music()

    def injectUiIpcChannel(self, uiIpcChannel):
        print("MusicPlayerServiceImpl : injectUiIpcChannel")
        self.__musicPlayerRepository.saveUiIpcChannel(uiIpcChannel)

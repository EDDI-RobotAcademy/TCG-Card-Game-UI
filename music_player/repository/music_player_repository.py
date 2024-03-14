import abc


class MusicPlayerRepository(abc.ABC):
    @abc.abstractmethod
    def saveUiIpcChannel(self, uiIpcChannel):
        pass

    @abc.abstractmethod
    def load_background_music_path_with_frame_name(self, frame_name: str):
        pass

    @abc.abstractmethod
    def load_sound_effect_path_with_event_name(self, event_name: str):
        pass

    @abc.abstractmethod
    def play_background_music(self):
        pass

    @abc.abstractmethod
    def play_sound_effect_with_event_name(self, event_name: str):
        pass

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

    @abc.abstractmethod
    def play_sound_effect_of_mouse_on_click(self, mouse_on_click_event_name: str):
        pass

    @abc.abstractmethod
    def play_sound_effect_of_battle_match(self, battle_match_event_name: str):
        pass

    @abc.abstractmethod
    def play_sound_effect_of_unit_deploy(self, deployed_unit_number: str):
        pass

    @abc.abstractmethod
    def play_sound_effect_of_unit_attack(self, unit_attack_event_name: str):
        pass

    @abc.abstractmethod
    def play_sound_effect_of_card_execution(self, card_execution_event_name: str):
        pass

    @abc.abstractmethod
    def play_sound_effect_of_timer(self, timer_event_name: str, stop_event: int):
        pass

    @abc.abstractmethod
    def play_sound_effect_of_game_end(self, game_end_event_name: str):
        pass

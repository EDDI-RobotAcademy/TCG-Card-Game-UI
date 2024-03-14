from battle_field.state.current_opponent_hp import CurrentOpponentHpState
from battle_field.state.opponent_main_character_survival_state import OpponentMainCharacterSurvivalState


class OpponentHpRepository:
    __instance = None

    current_hp_state = CurrentOpponentHpState()
    survival_state = OpponentMainCharacterSurvivalState()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def set_first_hp_state(self):
        self.current_hp_state.reset_health()

    def get_current_opponent_hp_state(self):
        return self.current_hp_state

    def take_damage(self, damage=5):
        print("take damaged!!!")
        self.current_hp_state.damage_to_hp(damage)
        # if self.current_hp_state.get_current_health() == 0:
        #     self.survival_state.character_die()

    def change_opponent_hp(self, new_hp):
        self.current_hp_state.set_health(new_hp)

    def get_opponent_character_survival_state(self):
        return self.survival_state

    def get_opponent_character_survival_info(self):
        return self.survival_state.get_character_survival_info()

    def opponent_character_die(self):
        self.survival_state.character_die()


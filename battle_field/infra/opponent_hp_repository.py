from battle_field.state.current_opponent_hp import CurrentOpponentHpState


class OpponentHpRepository:
    __instance = None

    current_hp_state = CurrentOpponentHpState()

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

    def change_opponent_hp(self, new_hp):
        self.current_hp_state.set_health(new_hp)
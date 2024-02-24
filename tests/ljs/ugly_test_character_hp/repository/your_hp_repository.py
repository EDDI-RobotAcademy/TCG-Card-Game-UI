from tests.ljs.ugly_test_character_hp.state.current_your_hp import CurrentYourHpState


class YourHpRepository:
    __instance = None

    current_hp_state = CurrentYourHpState()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def set_first_hp_state(self, hp):
        self.current_hp_state.reset_health()

    def get_current_your_hp_state(self):
        return self.current_hp_state

    def take_damage(self):
        self.current_hp_state.damage_to_hp(5)
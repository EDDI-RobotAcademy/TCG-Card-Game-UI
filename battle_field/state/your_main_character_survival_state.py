from common.survival_type import SurvivalType


class YourMainCharacterSurvivalState:
    def __init__(self):
        self.character_survival_info = SurvivalType.SURVIVAL

    def character_survive(self):
        self.character_survival_info = SurvivalType.SURVIVAL

    def character_die(self):
        self.character_survival_info = SurvivalType.DEATH

    def character_immortality(self):
        self.character_survival_info = SurvivalType.IMMORTAL

    def get_character_survival_info(self):
        return self.character_survival_info
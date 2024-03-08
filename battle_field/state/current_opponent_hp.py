class CurrentOpponentHpState:
    def __init__(self):
        self.health = 100

    def get_current_health(self):
        return self.health

    def damage_to_hp(self, damage):
        self.health -= damage

    def reset_health(self):
        self.health = 100

    def set_health(self, health):
        self.health = health

from battle_field.state.your_field_energy_state import YourFieldEnergyState


class YourFieldEnergyRepository:
    __instance = None

    your_field_energy_state = YourFieldEnergyState()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def increase_your_field_energy(self, count):
        self.your_field_energy_state.increase_field_energy(count)

    def decrease_your_field_energy(self, count):
        self.your_field_energy_state.decrease_field_energy(count)

    def get_your_field_energy(self):
        return self.your_field_energy_state.get_your_field_energy_count()



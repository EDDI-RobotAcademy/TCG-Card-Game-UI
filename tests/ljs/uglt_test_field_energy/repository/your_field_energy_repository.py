from tests.ljs.uglt_test_field_energy.state.current_your_field_energy import CurrentYourFieldEnergyState


class YourFieldEnergyRepositoryForTest:
    __instance = None

    current_energy_state = CurrentYourFieldEnergyState()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def reset_field_energy(self):
        self.current_energy_state.reset_current_your_field_energy()

    def get_current_your_field_energy_state(self):
        return self.current_energy_state

    def reduce_energy(self, count = 1):
        print("Energy Used!!!")
        self.current_energy_state.reduce_current_your_field_energy(count)

    def increase_energy(self, count = 1):
        self.current_energy_state.increase_current_your_field_energy(count)
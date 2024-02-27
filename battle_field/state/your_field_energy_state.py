class YourFieldEnergyState:
    def __init__(self):
        self.your_field_energy_count = 0

    def increase_field_energy(self, count):
        self.your_field_energy_count += count
        return True


    def decrease_field_energy(self, count):
        if self.your_field_energy_count - count >= 0:
            self.your_field_energy_count -= count
            return True
        else:
            self.your_field_energy_count = 0
            return False


    def get_your_field_energy_count(self):
        return self.your_field_energy_count


class CurrentYourFieldEnergyState:
    def __init__(self):
        self.field_energy_count = 0

    def reset_current_your_field_energy(self, field_energy_count=0):
        self.field_energy_count = field_energy_count

    def get_current_your_field_energy(self):
        return self.field_energy_count

    def reduce_current_your_field_energy(self, reduce_count):
        if self.field_energy_count > 0:
            self.field_energy_count -= reduce_count
            return True
        return False

    def increase_current_your_field_energy(self, increase_count):
        self.field_energy_count += increase_count



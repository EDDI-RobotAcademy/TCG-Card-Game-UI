class FieldEnergyState:
    def __init__(self):
        self.your_field_energy_count = 0
        self.opponent_field_energy_count = 0

    def increase_your_field_energy(self, count):
        # print(f"increase_your_field_energy -> count: {count}, self.your_field_energy_count: {self.your_field_energy_count}")
        self.your_field_energy_count += count
        return True


    def decrease_your_field_energy(self, count):
        if self.your_field_energy_count - count >= 0:
            self.your_field_energy_count -= count
            return True
        else:
            self.your_field_energy_count = 0
            return False


    def get_your_field_energy_count(self):
        return self.your_field_energy_count

    def increase_opponent_field_energy(self, count):
        # print(f"increase_opponent_field_energy -> count: {count}, self.opponent_field_energy_count: {self.opponent_field_energy_count}")
        self.opponent_field_energy_count += count
        return True

    def decrease_opponent_field_energy(self, count):
        if self.opponent_field_energy_count - count >= 0:
            self.opponent_field_energy_count -= count
            return True
        else:
            self.opponent_field_energy_count = 0
            return False

    def get_opponent_field_energy_count(self):
        return self.opponent_field_energy_count


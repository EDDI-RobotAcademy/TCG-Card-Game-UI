from collections import defaultdict


class AttachedExtraEnergyInfoState:
    def __init__(self):
        self.attached_extra_energy_info = {}
        self.attached_extra_energy_info_dictionary = {}

    def add_race_energy_at_index(self, index, energy_type, energy_quantity):
        print(f"first self.attached_energy_info: {self.attached_extra_energy_info}")
        if index not in self.attached_extra_energy_info:
            self.attached_extra_energy_info[index] = []
        print(f"add_race_energy_at_index() -> self.attached_energy_info: {self.attached_extra_energy_info}")
        print(f"self.attached_energy_info[index]: {self.attached_extra_energy_info[index]}")
        self.attached_extra_energy_info[index].append((energy_type, energy_quantity))
        print(f"After self.attached_energy_info[index].append((energy_type, energy_quantity)) -> self.attached_energy_info: {self.attached_extra_energy_info}")

    def remove_race_energy_at_index(self, index, energy_type, energy_quantity):
        if index in self.attached_extra_energy_info:
            self.attached_extra_energy_info[index] = [(t, q - energy_quantity) for t, q in self.attached_extra_energy_info[index] if
                                                t != energy_type]

    def get_total_energy_at_index(self, index):
        print(f"get_total_energy_at_index -> index: {index}")
        print(f"get_total_energy_at_index.get(index, []) -> res: {self.attached_extra_energy_info.get(index, [])}")
        print(f"self.attached_energy_info_dictionary.get(index, 0): {self.attached_extra_energy_info_dictionary.get(index, 0)}")
        return sum(q for t, q in self.attached_extra_energy_info.get(index, [])) + self.attached_extra_energy_info_dictionary.get(
            index, 0)

    def get_energy_info_at_index(self, index):
        print(f"get_energy_info_at_index -> self.attached_energy_info: {self.attached_extra_energy_info}")
        print(f"get_energy_info_at_index -> self.attached_energy_info[index]: {self.attached_extra_energy_info[index]}")
        return self.attached_extra_energy_info.get(index, [])

    def get_race_energy_at_index(self, index, energy_type):
        print(f"Debug: get_race_energy_at_index -> index: {index}")
        print(f"Debug: get_race_energy_at_index -> self.attached_energy_info: {self.attached_extra_energy_info}")

        energy_info = self.attached_extra_energy_info.get(index, [])
        print(f"Debug: get_race_energy_at_index -> energy_info: {energy_info}")

        race_energy_count = sum(
            q for t, q in energy_info if getattr(t, 'value', t) == getattr(energy_type, 'value', energy_type))
        print(f"Debug: get_race_energy_at_index -> race_energy_count: {race_energy_count}")

        return race_energy_count


    def add_energy_at_index(self, index, energy_quantity):
        if index in self.attached_extra_energy_info_dictionary:
            self.attached_extra_energy_info_dictionary[index] += energy_quantity
        else:
            self.attached_extra_energy_info_dictionary[index] = energy_quantity

    def remove_energy_at_index(self, index, energy_quantity):
        if index in self.attached_extra_energy_info_dictionary:
            self.attached_extra_energy_info_dictionary[index] = max(0, self.attached_extra_energy_info_dictionary[index] - energy_quantity)

    def get_energy_at_index(self, index):
        return self.attached_extra_energy_info_dictionary.get(index, 0)

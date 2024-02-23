from collections import defaultdict


class AttachedEnergyInfoState:
    def __init__(self):
        self.attached_energy_info = defaultdict(lambda: defaultdict(int))
        self.attached_energy_info_dictionary = {}

    def add_race_energy_at_index(self, index, energy_type, energy_quantity):
        print(f"attached_energy_info: {self.attached_energy_info}")
        self.attached_energy_info[index][energy_type] += energy_quantity

    def remove_race_energy_at_index(self, index, energy_type, energy_quantity):
        self.attached_energy_info[index][energy_type] = max(0, self.attached_energy_info[index][
            energy_type] - energy_quantity)

    def get_race_energy_at_index(self, index, energy_type):
        return self.attached_energy_info[index][energy_type]

    def add_energy_at_index(self, index, energy_quantity):
        if index in self.attached_energy_info_dictionary:
            self.attached_energy_info_dictionary[index] += energy_quantity
        else:
            self.attached_energy_info_dictionary[index] = energy_quantity

    def remove_energy_at_index(self, index, energy_quantity):
        if index in self.attached_energy_info_dictionary:
            self.attached_energy_info_dictionary[index] = max(0, self.attached_energy_info_dictionary[index] - energy_quantity)

    def get_energy_at_index(self, index):
        return self.attached_energy_info_dictionary.get(index, 0)


# class AttachedEnergyInfoState:
#     def __init__(self):
        # Dictionary는 index(0, 1, 2, 3)를 key 값으로 붙어 있는 에너지 수량(숫자)를 value로 사용
        # self.attached_energy_info_dictionary = {}

    # def add_energy_at_index(self, index, energy_quantity):
    #     if index in self.attached_energy_info_dictionary:
    #         self.attached_energy_info_dictionary[index] += energy_quantity
    #     else:
    #         self.attached_energy_info_dictionary[index] = energy_quantity
    #
    # def remove_energy_at_index(self, index, energy_quantity):
    #     if index in self.attached_energy_info_dictionary:
    #         self.attached_energy_info_dictionary[index] = max(0, self.attached_energy_info_dictionary[index] - energy_quantity)
    #
    # def get_energy_at_index(self, index):
    #     return self.attached_energy_info_dictionary.get(index, 0)

    # def add_energy_at_index(self, index, energy_type, energy_quantity):
    #     if index in self.attached_energy_info_dictionary:
    #         if energy_type in self.attached_energy_info_dictionary[index]:
    #             self.attached_energy_info_dictionary[index][energy_type] += energy_quantity
    #         else:
    #             self.attached_energy_info_dictionary[index][energy_type] = energy_quantity
    #     else:
    #         self.attached_energy_info_dictionary[index] = {energy_type: energy_quantity}
    #
    # def remove_energy_at_index(self, index, energy_type, energy_quantity):
    #     if index in self.attached_energy_info_dictionary:
    #         if energy_type in self.attached_energy_info_dictionary[index]:
    #             self.attached_energy_info_dictionary[index][energy_type] = max(
    #                 0, self.attached_energy_info_dictionary[index][energy_type] - energy_quantity)
    #
    # def get_energy_at_index(self, index):
    #     return self.attached_energy_info_dictionary.get(index, {})

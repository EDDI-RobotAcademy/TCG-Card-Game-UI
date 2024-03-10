class ExtraEffectInfo:
    def __init__(self):
        self.extra_effect_info = {}

    def update_extra_effect_of_unit(self, unit_index, extra_effect_list):
        print(f"update_extra_effect_of_unit: index - {unit_index}")
        print(f"current_extra_effect_info: {self.extra_effect_info}")
        self.extra_effect_info.update()
        if unit_index not in self.extra_effect_info.keys():
            self.extra_effect_info[unit_index] = []
            self.extra_effect_info[unit_index] = extra_effect_list
        else:
            self.extra_effect_info[unit_index] = extra_effect_list

        print(f"updated_extra_effect_info: {self.extra_effect_info}")

    def get_extra_effect_of_index(self, unit_index):
        return self.extra_effect_info[unit_index]

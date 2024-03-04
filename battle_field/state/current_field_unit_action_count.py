class CurrentFieldUnitActionCountState:
    def __init__(self):
        self.your_field_unit_list_action_count = []

    def reset_your_field_unit_list_action_count(self):
        for index in range(len(self.your_field_unit_list_action_count)):
            if self.your_field_unit_list_action_count == -1:
                continue

            self.your_field_unit_list_action_count[index] = 1

    def use_field_unit_action_count_by_index(self, index):
        self.your_field_unit_list_action_count[index] -= 1

    def get_your_field_unit_list_action_count(self, index):
        return self.your_field_unit_list_action_count[index]

    def set_your_field_unit_list_action_count(self, index, count):
        self.your_field_unit_list_action_count[index] = count

    def make_field_unit_action_count(self, count):
        self.your_field_unit_list_action_count.append(count)


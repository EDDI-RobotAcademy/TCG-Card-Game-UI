from battle_field.state.FieldUnitActionStatus import FieldUnitActionStatus


class CurrentFieldUnitActionStatus:
    def __init__(self):
        self.your_field_unit_action_status_list = []

    def create_your_field_unit_action(self):
        self.your_field_unit_action_status_list.append(FieldUnitActionStatus.WAIT)

    def set_your_field_unit_action_status_at_index(self, index, status):
        self.your_field_unit_action_status_list[index] = status

    def get_your_field_unit_action_status_at_index(self, index):
        return self.your_field_unit_action_status_list[index]


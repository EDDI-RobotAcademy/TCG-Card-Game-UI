class CurrentFieldUnitState:
    def __init__(self):
        self.current_field_unit_list = []

    def place_unit_to_field(self, unit):
        self.current_field_unit_list.append(unit)

    def get_current_field_unit_list(self):
        return self.current_field_unit_list


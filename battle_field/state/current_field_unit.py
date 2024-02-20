class CurrentFieldUnitState:
    def __init__(self):
        self.current_field_unit_list = []

    def place_unit_to_field(self, unit):
        self.current_field_unit_list.append(unit)

    def get_current_field_unit_list(self):
        return self.current_field_unit_list

    def delete_current_field_unit_list(self, unit_index):
        if 0 <= unit_index < len(self.current_field_unit_list):
            del self.current_field_unit_list[unit_index]
            print(f"Unit at index {unit_index} 삭제")
        else:
            print(f"Invalid index: {unit_index}. No unit!")


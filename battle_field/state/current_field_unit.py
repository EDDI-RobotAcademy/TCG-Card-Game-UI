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

    def remove_from_field(self, *cards):
        for card in cards:
            if card in self.current_field_unit_list:
                self.current_field_unit_list.remove(card)
            else:
                print(f"Card '{card}' not found in the current hand.")

    def remove_field_unit_by_index(self, index):
        if 0 <= index < len(self.current_field_unit_list):
            removed_card = self.current_field_unit_list.pop(index)
            print(f"Removed card index {index}: {removed_card}")
        else:
            print(f"Invalid index: {index}. 지울 것이 없다")
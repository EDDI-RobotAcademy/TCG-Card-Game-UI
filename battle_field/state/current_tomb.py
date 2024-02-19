class CurrentTombState:
    def __init__(self):
        self.current_tomb_unit_list = []

    def place_unit_to_tomb(self, unit):
        self.current_tomb_unit_list.append(unit)

    def get_current_tomb_unit_list(self):
        return self.current_tomb_unit_list

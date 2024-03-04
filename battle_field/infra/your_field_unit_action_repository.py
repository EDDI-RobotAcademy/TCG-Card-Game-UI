from battle_field.state.current_field_unit_action_count import CurrentFieldUnitActionCountState
from battle_field.state.current_field_unit_action_status import CurrentFieldUnitActionStatus


class CurrentFieldUnitActionRepository:
    __instance = None

    current_field_unit_action_count = CurrentFieldUnitActionCountState()
    current_field_unit_action_status = CurrentFieldUnitActionStatus()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def create_field_unit_action_count(self, count):
        self.current_field_unit_action_count.make_field_unit_action_count(count)
        print(f"create_field_unit_action_count_by_index() -> count {count}")

    def get_current_field_unit_action_count(self):
        return self.current_field_unit_action_count.get_your_field_unit_list_action_count()




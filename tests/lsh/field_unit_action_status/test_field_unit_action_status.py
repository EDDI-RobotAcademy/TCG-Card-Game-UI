import unittest

from battle_field.state.FieldUnitActionStatus import FieldUnitActionStatus
from battle_field.state.current_field_unit_action_status import CurrentFieldUnitActionStatus


class TestCurrentFieldUnitActionStatus(unittest.TestCase):
    def setUp(self):
        self.status_instance = CurrentFieldUnitActionStatus()

    def test_set_and_get_your_field_unit_action_status_at_index(self):
        self.status_instance.create_your_field_unit_action()
        self.assertEqual(self.status_instance.get_your_field_unit_action_status_at_index(0), FieldUnitActionStatus.WAIT)

        self.status_instance.set_your_field_unit_action_status_at_index(0, FieldUnitActionStatus.READY)
        self.assertEqual(self.status_instance.get_your_field_unit_action_status_at_index(0), FieldUnitActionStatus.READY)

    def test_get_your_field_unit_action_status_at_index_with_invalid_index(self):
        with self.assertRaises(IndexError):
            self.status_instance.get_your_field_unit_action_status_at_index(5)

if __name__ == '__main__':
    unittest.main()

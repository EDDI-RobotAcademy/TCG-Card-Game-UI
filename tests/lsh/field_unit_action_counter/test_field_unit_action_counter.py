import unittest

from battle_field.state.current_field_unit_action_count import CurrentFieldUnitActionCountState


class TestCurrentFieldUnitActionCountState(unittest.TestCase):
    def setUp(self):
        self.state = CurrentFieldUnitActionCountState()

    def test_reset_your_field_unit_list_action_count(self):
        self.state.reset_your_field_unit_list_action_count()
        self.assertEqual(self.state.get_your_field_unit_list_action_count(), [])

        self.state.your_field_unit_list_action_count = [2, 3, 1]
        self.state.reset_your_field_unit_list_action_count()
        self.assertEqual(self.state.get_your_field_unit_list_action_count(), [1, 1, 1])

    def test_use_field_unit_action_count_by_index(self):
        self.state.your_field_unit_list_action_count = [2, 3, 1]
        self.state.use_field_unit_action_count_by_index(1)
        self.assertEqual(self.state.get_your_field_unit_list_action_count(), [2, 2, 1])

        self.state.use_field_unit_action_count_by_index(2)
        self.assertEqual(self.state.get_your_field_unit_list_action_count(), [2, 2, 0])

    def test_make_field_unit_action_count(self):
        self.state.make_field_unit_action_count(3)
        self.assertEqual(self.state.get_your_field_unit_list_action_count(), [3])

        self.state.your_field_unit_list_action_count = [2, 3, 1]
        self.assertEqual(self.state.get_your_field_unit_list_action_count(), [2, 3, 1])


if __name__ == '__main__':
    unittest.main()

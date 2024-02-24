import unittest
from collections import defaultdict

from battle_field.state.attached_energy_info import AttachedEnergyInfoState
from battle_field.state.energy_type import EnergyType


class TestAttachedEnergyInfoState(unittest.TestCase):
    def setUp(self):
        self.energy_state = AttachedEnergyInfoState()

    def test_add_energy_at_index(self):
        self.energy_state.add_energy_at_index(0, EnergyType.Undead, 5)
        self.assertEqual(self.energy_state.attached_energy_info[0][EnergyType.Undead], 5)

        self.energy_state.add_energy_at_index(0, EnergyType.Undead, 3)
        self.assertEqual(self.energy_state.attached_energy_info[0][EnergyType.Undead], 8)

        self.energy_state.add_energy_at_index(0, EnergyType.Human, 2)
        self.assertEqual(self.energy_state.attached_energy_info[0][EnergyType.Human], 2)

    def test_remove_energy_at_index(self):
        self.energy_state.add_energy_at_index(1, EnergyType.Undead, 8)

        self.energy_state.remove_energy_at_index(1, EnergyType.Undead, 3)
        self.assertEqual(self.energy_state.attached_energy_info[1][EnergyType.Undead], 5)

        self.energy_state.remove_energy_at_index(1, EnergyType.Undead, 7)
        self.assertEqual(self.energy_state.attached_energy_info[1][EnergyType.Undead], 0)

        self.energy_state.remove_energy_at_index(1, EnergyType.Human, 2)
        self.assertEqual(self.energy_state.attached_energy_info[1][EnergyType.Human], 0)

    def test_get_energy_at_index(self):
        self.assertEqual(self.energy_state.get_energy_at_index(2, EnergyType.Undead), 0)

        self.energy_state.add_energy_at_index(2, EnergyType.Undead, 10)
        self.assertEqual(self.energy_state.get_energy_at_index(2, EnergyType.Undead), 10)

        self.assertEqual(self.energy_state.get_energy_at_index(2, EnergyType.Human), 0)


if __name__ == '__main__':
    unittest.main()

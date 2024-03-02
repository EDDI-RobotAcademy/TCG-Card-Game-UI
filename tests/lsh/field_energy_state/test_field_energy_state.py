import unittest

from battle_field.state.field_energy_state import YourFieldEnergyState


class TestYourFieldEnergyState(unittest.TestCase):
    def test_initial_energy_count(self):
        state = YourFieldEnergyState()
        self.assertEqual(state.get_your_field_energy_count(), 0)

    def test_increase_energy(self):
        state = YourFieldEnergyState()
        state.increase_field_energy(5)
        self.assertEqual(state.get_your_field_energy_count(), 5)

    def test_decrease_energy(self):
        state = YourFieldEnergyState()
        state.increase_field_energy(10)
        state.decrease_field_energy(3)
        self.assertEqual(state.get_your_field_energy_count(), 7)

    def test_negative_energy(self):
        state = YourFieldEnergyState()
        state.decrease_field_energy(5)
        self.assertEqual(state.get_your_field_energy_count(), -5)

if __name__ == '__main__':
    unittest.main()

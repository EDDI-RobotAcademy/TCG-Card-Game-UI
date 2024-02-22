import unittest

from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository


class TestYourFieldEnergyRepository(unittest.TestCase):
    def setUp(self):
        YourFieldEnergyRepository.__instance = None

    def test_increase_energy(self):
        repository = YourFieldEnergyRepository.getInstance()
        repository.increase_your_field_energy(5)
        self.assertEqual(repository.get_your_field_energy(), 5)

    def test_decrease_energy(self):
        repository = YourFieldEnergyRepository.getInstance()
        repository.increase_your_field_energy(10)
        repository.decrease_your_field_energy(3)
        self.assertEqual(repository.get_your_field_energy(), 7)

    def test_negative_energy(self):
        repository = YourFieldEnergyRepository.getInstance()
        repository.decrease_your_field_energy(5)
        self.assertEqual(repository.get_your_field_energy(), -5)

if __name__ == '__main__':
    unittest.main()

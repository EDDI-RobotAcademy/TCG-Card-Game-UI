import unittest

from battle_field.infra.legacy.circle_image_legacy_your_field_unit_repository import CircleImageLegacyYourFieldUnitRepository
from battle_field.state.attached_energy_info import AttachedEnergyInfoState
from initializer.init_domain import DomainInitializer


class TestAttachedEnergyInfoState(unittest.TestCase):

    def test_attach_energy_at_index(self):
        energy_info_state = AttachedEnergyInfoState()

        energy_info_state.add_energy_at_index(1, 5)
        self.assertEqual(energy_info_state.get_energy_at_index(1), 5)

        energy_info_state.add_energy_at_index(1, 3)
        self.assertEqual(energy_info_state.get_energy_at_index(1), 8)

        energy_info_state.add_energy_at_index(3, 2)
        self.assertEqual(energy_info_state.get_energy_at_index(3), 2)

    def test_remove_energy_at_index(self):
        energy_info_state = AttachedEnergyInfoState()

        energy_info_state.add_energy_at_index(0, 10)
        energy_info_state.remove_energy_at_index(0, 5)
        self.assertEqual(energy_info_state.get_energy_at_index(0), 5)

        energy_info_state.remove_energy_at_index(0, 8)
        self.assertEqual(energy_info_state.get_energy_at_index(0), 0)

    def test_get_energy_at_index(self):
        energy_info_state = AttachedEnergyInfoState()
        self.assertEqual(energy_info_state.get_energy_at_index(2), 0)

        energy_info_state.add_energy_at_index(2, 7)
        self.assertEqual(energy_info_state.get_energy_at_index(2), 7)

    def test_attach_energy(self):
        DomainInitializer.initEachDomain()
        field_unit_repository = CircleImageLegacyYourFieldUnitRepository.getInstance()

        field_unit_repository.create_field_unit_card(8)
        field_unit_repository.attach_energy(0, 3)
        self.assertEqual(field_unit_repository.attached_energy_info.get_energy_at_index(0), 3)

        field_unit_repository.attach_energy(0, 2)
        self.assertEqual(field_unit_repository.attached_energy_info.get_energy_at_index(0), 5)

        field_unit_repository.attach_energy(1, 4)
        self.assertEqual(field_unit_repository.attached_energy_info.get_energy_at_index(1), 4)

    def test_detach_energy(self):
        DomainInitializer.initEachDomain()
        field_unit_repository = CircleImageLegacyYourFieldUnitRepository.getInstance()

        field_unit_repository.create_field_unit_card(6)
        field_unit_repository.attach_energy(0, 7)
        field_unit_repository.detach_energy(0, 3)
        self.assertEqual(field_unit_repository.attached_energy_info.get_energy_at_index(0), 4)

        field_unit_repository.detach_energy(1, 6)
        self.assertEqual(field_unit_repository.attached_energy_info.get_energy_at_index(1), 0)

if __name__ == '__main__':
    unittest.main()

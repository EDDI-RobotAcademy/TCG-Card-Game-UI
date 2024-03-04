import unittest

from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field_fixed_card.fixed_field_card import LegacyFixedFieldCard
from initializer.init_domain import DomainInitializer


class TestHandStateToFieldUnit(unittest.TestCase):

    def test_hand_state_to_field_unit(self):
        DomainInitializer.initEachDomain()

        self.your_hand_repository = YourHandRepository.getInstance()
        self.your_hand_repository.save_current_hand_state([6, 8, 19, 151])
        self.your_hand_repository.create_hand_card_list()

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()

        for hand_card in self.hand_card_list:
            print(f"hand_card id: {hand_card.get_card_number()}")

        self.field_unit_repository = YourFieldUnitRepository.getInstance()
        self.field_unit_repository.save_current_field_unit_state(self.hand_card_list[0].get_card_number())

        print(f"state: {self.field_unit_repository.get_current_field_unit_state()}")
        # self.field_unit_repository.create_field_unit_card_list()

        # self.battle_field_unit = FixedFieldCard(local_translation=(300, 580))
        # self.battle_field_unit.init_card(32)




if __name__ == '__main__':
    unittest.main()
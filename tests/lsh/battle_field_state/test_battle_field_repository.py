import unittest
from unittest.mock import patch

from battle_field.infra.battle_field_repository import BattleFieldRepository


class TestBattleFieldRepository(unittest.TestCase):

    def setUp(self):
        self.battle_field_repository = BattleFieldRepository()

    def test_save_and_get_current_hand_state(self):
        hand_list = ["Card1", "Card2", "Card3"]
        self.battle_field_repository.save_current_hand_state(hand_list)
        retrieved_hand_state = self.battle_field_repository.get_current_hand_state()
        self.assertEqual(retrieved_hand_state, [hand_list])

    def test_save_and_get_current_deck_state(self):
        deck_list = ["Card4", "Card5", "Card6"]
        self.battle_field_repository.save_current_deck_state(deck_list)
        retrieved_deck_state = self.battle_field_repository.get_current_deck_state()
        self.assertEqual(retrieved_deck_state, [deck_list])

    def test_save_empty_current_hand_state(self):
        empty_hand_list = []
        self.battle_field_repository.save_current_hand_state(empty_hand_list)
        retrieved_hand_state = self.battle_field_repository.get_current_hand_state()
        self.assertEqual(retrieved_hand_state, [[]])

    def test_save_empty_current_deck_state(self):
        empty_deck_list = []
        self.battle_field_repository.save_current_deck_state(empty_deck_list)
        retrieved_deck_state = self.battle_field_repository.get_current_deck_state()
        self.assertEqual(retrieved_deck_state, [[]])


if __name__ == '__main__':
    unittest.main()

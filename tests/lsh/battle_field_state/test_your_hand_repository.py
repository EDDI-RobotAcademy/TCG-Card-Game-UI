import unittest
from unittest.mock import patch, MagicMock, call

from battle_field.infra.your_hand_repository import YourHandRepository
from initializer.init_domain import DomainInitializer
from opengl_battle_field_card.card import Card


class TestYourHandRepository(unittest.TestCase):

    def setUp(self):
        DomainInitializer.initEachDomain()
        self.repository = YourHandRepository.getInstance()

    @patch('battle_field.state.current_hand.CurrentHandState.add_to_hand')
    def test_save_current_hand_state(self, mock_add_to_hand):
        hand_list = [1, 2, 3]
        self.repository.save_current_hand_state(hand_list)
        mock_add_to_hand.assert_called_with(hand_list)

    @patch('battle_field.state.current_hand.CurrentHandState.get_current_hand')
    def test_get_current_hand_state(self, mock_get_current_hand):
        expected_result = [1, 2, 3]
        mock_get_current_hand.return_value = expected_result
        result = self.repository.get_current_hand_state()
        self.assertEqual(result, expected_result)

    def test_save_and_get_current_hand_state(self):
        hand_list = ["Card1", "Card2", "Card3"]
        self.repository.save_current_hand_state(hand_list)
        retrieved_hand_state = self.repository.get_current_hand_state()
        self.assertEqual(retrieved_hand_state, [hand_list])

    def test_save_empty_current_hand_state(self):
        empty_hand_list = []
        self.repository.save_current_hand_state(empty_hand_list)
        retrieved_hand_state = self.repository.get_current_hand_state()
        self.assertEqual(retrieved_hand_state, [[]])

    def test_get_next_card_position(self):
        result = self.repository.get_next_card_position()
        # Replace with your actual logic to determine the next card position
        expected_result = (100, 100)
        self.assertEqual(result, expected_result)

    def test_get_current_hand_card_list(self):
        # Assuming you have a card list populated in the repository
        self.repository.current_hand_card_list = ['card1', 'card2', 'card3']
        result = self.repository.get_current_hand_card_list()
        expected_result = ['card1', 'card2', 'card3']
        self.assertEqual(result, expected_result)

    def test_create_hand_card_list(self):
        DomainInitializer.initEachDomain()

        repository = YourHandRepository()
        # repository.current_hand_state.current_hand_list = [6, 8]

        repository.save_current_hand_state([6, 8])

        repository.create_hand_card_list()
        expected_card_list = [Card(local_translation=(100, 100)) for _ in range(2)]

if __name__ == '__main__':
    unittest.main()

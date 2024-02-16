import unittest

from battle_field.state.current_deck import CurrentDeck


class TestCurrentDeck(unittest.TestCase):

    def setUp(self):
        self.current_deck = CurrentDeck()

    def test_add_to_deck(self):
        self.current_deck.add_to_deck("Card1", "Card2")
        self.assertEqual(self.current_deck.get_deck_size(), 2)

        self.current_deck.add_to_deck("Card3")
        self.assertEqual(self.current_deck.get_deck_size(), 3)

    def test_draw_card(self):
        self.current_deck.add_to_deck("Card1", "Card2", "Card3")

        drawn_card = self.current_deck.draw_card()
        self.assertEqual(drawn_card, "Card1")
        self.assertEqual(self.current_deck.get_deck_size(), 2)

        self.current_deck.draw_card()

    def test_get_deck_size(self):
        self.assertEqual(self.current_deck.get_deck_size(), 0)

        self.current_deck.add_to_deck("Card1", "Card2", "Card3")
        self.assertEqual(self.current_deck.get_deck_size(), 3)

    def test_empty_deck(self):
        self.assertIsNone(self.current_deck.draw_card())
        self.assertEqual(self.current_deck.get_deck_size(), 0)


if __name__ == '__main__':
    unittest.main()

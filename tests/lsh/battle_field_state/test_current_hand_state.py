import unittest

from battle_field.state.current_hand import CurrentHand


class TestCurrentHand(unittest.TestCase):

    def setUp(self):
        self.current_hand = CurrentHand()

    def test_add_to_hand(self):
        self.current_hand.add_to_hand("Card1")
        self.assertEqual(self.current_hand.get_current_hand(), ["Card1"])

        self.current_hand.add_to_hand("Card2", "Card3")
        self.assertEqual(self.current_hand.get_current_hand(), ["Card1", "Card2", "Card3"])

    def test_remove_from_hand(self):
        self.current_hand.add_to_hand("Card1", "Card2", "Card3")

        self.current_hand.remove_from_hand("Card2")
        self.assertEqual(self.current_hand.get_current_hand(), ["Card1", "Card3"])

        self.current_hand.remove_from_hand("Card4")
        self.assertEqual(self.current_hand.get_current_hand(), ["Card1", "Card3"])

        self.current_hand.remove_from_hand("Card1", "Card3")
        self.assertEqual(self.current_hand.get_current_hand(), [])

    def test_clear_current_hand(self):
        self.current_hand.add_to_hand("Card1", "Card2", "Card3")
        self.current_hand.clear_current_hand()
        self.assertEqual(self.current_hand.get_current_hand(), [])


if __name__ == '__main__':
    unittest.main()

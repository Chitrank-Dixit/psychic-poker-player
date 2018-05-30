import unittest
from psychic_poker import Poker


class TestPokerBestHand(unittest.TestCase):
    """
        Test module for testing best poker hands
    """
    def setUp(self):
        """
            In this we will feed the result data that needs to be matched
        """
        self.test_data_results = list(range(0, 9))

    def test_poker_best_hands(self):
        """
            Test for the best poker hands possible
        """
        with open("poker_input", 'r') as file:
            for counter, line in enumerate(file):
                data = line.split(" ")
                data[-1] = data[-1].split("\n")[0]
                p1 = Poker(data)
                best_of_hands = None
                best_hand_list = []
                for current_hand in p1.get_poker_hands():
                    best_hand = p1.check_for_best_hand(current_hand)
                    best_hand_list.append(best_hand)
                    if best_of_hands == None or best_hand < best_of_hands:
                        best_of_hands = best_hand
                    if best_of_hands == 0:
                        break
                assert best_of_hands == self.test_data_results[counter]

if __name__ == '__main__':
    unittest.main()
from itertools import combinations
import sys

"""

Best of Poker hands

1	Straight flush**	JC TC 9C 8C 7C
2	Four of a kind	    5C 5D 5H 5S 2D
3	Full house	        6S 6H 6D KC KH
4	Flush**	            JD 9D 8D 4D 3D
5	Straight**	        TD 9S 8H 7D 6C
6	Three of a kind	    QC QS QH 9H 2S
7	Two pair	        JH JS 3C 3S 2H
8	One pair	        TS TH 8S 7H 4C
9	High card	        KD QD 7S 4S 3H

"""

SUIT_RANK = {"S": 4, "H": 3, "D": 2, "C": 1}

CARD_RANK = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10, "9": 9,
             "8": 8, "7": 7, "6": 6, "5": 5, "4": 4,
             "3": 3, "2": 2}

REVERSE_CARD_RANK_MAPPING = {"14": "A", "13": "K", "12": "Q", "11": "J", "10": "T"}

win_priority_list = ["straight-flush", "four-of-a-kind", "full-house", "flush", "straight",
                     "three-of-a-kind", "two-pairs", "one-pair", "highest-card"]


class Poker:
    """
        Poker game to ensure the player gets the best hand
    """

    def __init__(self, input_data):
        """

        :param input_data: list of all the card in hand and deck
        """
        self.input_data = input_data
        self.hand = self.input_data[:5]
        self.deck = self.input_data[5:]

    @classmethod
    def reinitialize_hand_card_rank(cls):
        """

        :return: return hand_cards_value dictionary , counters initialized to 0
        """
        hand_cards_value = {"A": 0, "K": 0, "Q": 0, "J": 0, "T": 0, "9": 0,
                            "8": 0, "7": 0, "6": 0, "5": 0, "4": 0,
                            "3": 0, "2": 0}
        return hand_cards_value

    def get_poker_hands(self):
        """
            This function would yield a possible hand, discarding
            some cards in the hand and getting some cards from the
            deck, we need to get the possible combinations
        """
        for cards_in_hand in range(1, len(self.hand) + 1):
            for replace in combinations(range(len(self.hand)), cards_in_hand):
                possible_hand = self.hand[:]
                for deck_offset, replace_offset in enumerate(replace):
                    possible_hand[replace_offset] = self.deck[deck_offset]
                    yield possible_hand

    def check_for_best_hand(self, hand):
        """

        :param hand: cards in hand , hand is a list of cards
        :return: return the best possible hand , the lowest value the better one
        """
        best_possible_hand = 8
        if self.check_for_straight_flush(hand):
            best_possible_hand = 0
        elif self.check_for_four_of_a_kind(hand):
            best_possible_hand = 1
        elif self.check_for_full_house(hand):
            best_possible_hand = 2
        elif self.check_for_flush(hand):
            best_possible_hand = 3
        elif self.check_for_straight(hand):
            best_possible_hand = 4
        elif self.check_for_three_of_a_kind(hand):
            best_possible_hand = 5
        elif self.check_for_two_pairs(hand):
            best_possible_hand = 6
        elif self.check_for_one_pair(hand):
            best_possible_hand = 7
        return best_possible_hand

    def check_for_straight_flush(self, hand):
        """

        :param hand: cards in hand , hand is a list of cards
        :return: True: straight-flush, False otherwise
        """
        return self.check_for_flush(hand) and self.check_for_straight(hand)

    def check_for_four_of_a_kind(self, hand):
        """

        :param hand: cards in hand , hand is a list of cards
        :return: True: four-of-a-kind, False otherwise
        """
        card_ranks = [card[0] for card in hand]
        for card in card_ranks:
            if card_ranks.count(card) == 4:
                return True
        return False

    def check_for_full_house(self, hand):
        """

        :param hand: cards in hand , hand is a list of cards
        :return: True: full-house, False otherwise
        """
        hand_cards_value = {"A": 0, "K": 0, "Q": 0, "J": 0, "T": 0, "9": 0,
                            "8": 0, "7": 0, "6": 0, "5": 0, "4": 0,
                            "3": 0, "2": 0}

        for element in hand:
            hand_cards_value[element[0]] += 1

        tuple_card = ""
        triple_card = ""
        for key, value in hand_cards_value.items():
            if value == 2:
                tuple_card = key
            elif value == 3:
                triple_card = key

        if tuple_card and triple_card:
            return True
        return False

    def check_for_flush(self, hand):
        """

        :param hand: cards in hand , hand is a list of cards
        :return: True: flush, False otherwise
        """
        selected_suit = hand[0][1]
        for card in hand:
            rank, suit = card[0], card[1]
            if selected_suit != suit:
                return False
        return True

    def check_for_straight(self, hand):
        """

        :param hand: cards in hand , hand is a list of cards
        :return: True: straigh, False otherwise
        """
        prev = 0
        card_with_ranks = sorted([CARD_RANK[card[0]] for card in hand])

        # for ace as higher card
        counter = 0
        for rank in card_with_ranks:
            if prev:
                if (rank - prev) == 1:
                    counter += 1
                else:
                    counter = 0
            prev = rank

        if counter == 4:
            return True

        # for ace as lower card
        counter = 0
        check_list = [2, 3, 4, 5, 14]
        for index, rank in enumerate(card_with_ranks):
            if rank == check_list[index]:
                counter += 1
            else:
                counter = 0

        if counter == 5:
            return True

        return False

    def check_for_three_of_a_kind(self, hand):
        """

        :param hand: cards in hand , hand is a list of cards
        :return: True: three-of-a-kind, False: otherwise
        """
        card_ranks = [card[0] for card in hand]
        for card in card_ranks:
            if card_ranks.count(card) == 3:
                return True
        return False

    def check_for_two_pairs(self, hand):
        """

        :param hand: cards in hand , hand is a list of cards
        :return: True: two-pairs, False: otherwise
        """

        hand_cards_rank = self.reinitialize_hand_card_rank()

        for element in hand:
            hand_cards_rank[element[0]] += 1

        tuple_card = ""
        card_value = 0
        for key, value in hand_cards_rank.items():
            if value == 2:
                card_value += value
            if card_value >= 4:
                tuple_card = key
        if tuple_card:
            return True
        return False

    def check_for_one_pair(self, hand):
        """

        :param hand: cards in hand , hand is a list of cards
        :return: True: one-pair, False: otherwise
        """

        hand_cards_rank = self.reinitialize_hand_card_rank()

        for element in hand:
            hand_cards_rank[element[0]] += 1

        tuple_card = ""
        for key, value in hand_cards_rank.items():
            if value == 2:
                tuple_card = key
        if tuple_card:
            return True
        return False


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as file:
        for line in file:
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
            print("Hand: " + " ".join(p1.hand) +
                  " Deck: " + " ".join(p1.deck) +
                  " Best hand: " + win_priority_list[best_of_hands])

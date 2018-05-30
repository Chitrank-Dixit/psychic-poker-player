from itertools import combinations

__author__ = 'chitrankdixit'
import copy
import sys

# This will ensure the correctness of the psychic poker

# poker hand
# class PokerHand:
#     """
#         PokerHand would check the occurance of the hand
#     """
#     def __init__(self, hand, deck):
#         self.hand = hand
#         self.deck = deck


"""

1	Straight flush**	Jack of clubs10 of clubs9 of clubs8 of clubs7 of clubs
2	Four of a kind	5 of clubs5 of diamonds5 of hearts5 of spades2 of diamonds
3	Full house	6 of spades6 of hearts6 of diamondsKing of clubsKing of hearts
4	Flush**	Jack of diamonds9 of diamonds8 of diamonds4 of diamonds3 of diamonds
5	Straight**	10 of diamonds9 of spades8 of hearts7 of diamonds6 of clubs
6	Three of a kind	Queen of clubsQueen of spadesQueen of hearts9 of hearts2 of spades
7	Two pair	Jack of heartsJack of spades3 of clubs3 of spades2 of hearts
8	One pair	10 of spades10 of hearts8 of spades7 of hearts4 of clubs
9	High card	King of diamondsQueen of diamonds7 of spades4 of spades3 of hearts

"""

SUIT_RANK = {"S": 4, "H": 3, "D": 2, "C": 1}
CARD_RANK = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10, "9": 9,
             "8": 8, "7": 7, "6": 6, "5": 5, "4": 4,
             "3": 3, "2": 2}
REVERSE_CARD_RANK_MAPPING = {"14": "A", "13": "K", "12": "Q", "11": "J", "10": "T"}

# Not needed
# CARD_VALUE_MAPPING = {}





win_priority_list = ["straight-flush", "four-of-a-kind", "full-house", "flush", "straight",
                     "three-of-a-kind", "two-pairs", "one-pair", "highest-card"]


class Poker:
    """
        Poker game to ensure the player gets the best hand
    """
    def __init__(self, input_data):
        self.input_data = input_data
        self.copied_list = copy.deepcopy(self.input_data)

    def split_hand_and_deck(self):
        self.hand = self.input_data[:5]
        self.deck = self.input_data[5:]

    def reinitialize_had_card_rank(self):
        hand_cards_rank = {"A": 0, "K": 0, "Q": 0, "J": 0, "T": 0, "9": 0,
             "8": 0, "7": 0, "6": 0, "5": 0, "4": 0,
             "3": 0, "2": 0}
        return hand_cards_rank

    def get_poker_hands(self):
        for cards_in_hand in range(1, len(self.hand) + 1):
            for replace in combinations(range(len(self.hand)), cards_in_hand):
                possible_hand = self.hand[:]
                for deck_offset, replace_offset in enumerate(replace):
                    possible_hand[replace_offset] = self.deck[deck_offset]
                    yield possible_hand

    def check_for_best_hand(self, current_hand):
        best_possible_hand = 8
        if self.check_for_straight_flush(current_hand):
            best_possible_hand = 0
        elif self.check_for_four_of_a_kind(current_hand):
            best_possible_hand = 1
        elif self.check_for_full_house(current_hand):
            best_possible_hand = 2
        elif self.check_for_flush(current_hand):
            best_possible_hand = 3
        elif self.check_for_straight(current_hand):
            best_possible_hand = 4
        elif self.check_for_three_of_a_kind(current_hand):
            best_possible_hand = 5
        elif self.check_for_two_pairs(current_hand):
            best_possible_hand = 6
        elif self.check_for_one_pair(current_hand):
            best_possible_hand = 7
        return best_possible_hand

    # TODO check for straight flush
    def check_for_straight_flush(self, hand):
        """
        :return:
        """
        return self.check_for_flush(hand) and self.check_for_straight(hand)

    # TODO check for four of a kind
    def check_for_four_of_a_kind(self, hand):

        card_ranks = [card[0] for card in hand]
        for card in card_ranks:
            if card_ranks.count(card) == 4:
                return True
        return False

    # TODO check for full house
    def check_for_full_house(self, hand):

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

    # TODO check for flush
    def check_for_flush(self, hand):
        """

        :return:
        """
        selected_suit = hand[0][1]
        for card in hand:
            rank, suit = card[0], card[1]
            if selected_suit != suit:
                return False
        return True

    def check_for_straight_match_count(self, count):
        return count == 5

    # TODO check for straight
    def check_for_straight(self, hand):
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
        check_list = [2,3,4,5,14]
        for rank in card_with_ranks:
            if rank in check_list:
                counter += 1
            else:
                counter  = 0

        if counter == 5:
            return True

        return False

    # TODO check for three of a kind
    def check_for_three_of_a_kind(self, hand):

        card_ranks = [card[0] for card in hand]
        for card in card_ranks:
            if card_ranks.count(card) == 3:
                return True
        return False

    # TODO check for two pairs
    def check_for_two_pairs(self, hand):
        """
            check for two pairs existence
        :return:
        """

        hand_cards_rank = self.reinitialize_had_card_rank()

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

    # TODO check for one pair
    def check_for_one_pair(self, hand):
        """
            check for one pair existence
        :return:
        """

        hand_cards_rank = self.reinitialize_had_card_rank()

        for element in hand:
            hand_cards_rank[element[0]] += 1

        tuple_card = ""
        card_value = 0
        for key, value in hand_cards_rank.items():
            if value == 2:
                tuple_card = key
        if tuple_card:
            return True
        return False


if __name__ == "__main__":
    input_list = []
    # card value mapping
    # NOT NEEDED
    # for key in CARD_RANK.keys():
    #     for inner_key in SUIT_RANK.keys():
    #         CARD_VALUE_MAPPING[key+inner_key] = SUIT_RANK[inner_key] + CARD_RANK[key]

    with open(sys.argv[1], 'r') as file:
        for counter, line in enumerate(file):
            data= line.split(" ")
            data[-1] = data[-1].split("\n")[0]
            p1 = Poker(data)
            p1.split_hand_and_deck()
            best_of_hands = None
            best_hand_list = []
            for counter, current_hand in enumerate(p1.get_poker_hands()):
                best_hand = p1.check_for_best_hand(current_hand)
                best_hand_list.append(best_hand)
                if best_of_hands == None or best_hand < best_of_hands:
                    best_of_hands = best_hand
            print("Hand: " + " ".join(p1.hand) + " Deck: "+ " ".join(p1.deck) + " Best hand: " + win_priority_list[best_of_hands])
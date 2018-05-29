__author__ = 'chitrankdixit'
from itertools import combinations, combinations_with_replacement
a = ["TH", "JH", "QC", "QD",  "QS", "QH", "KH", "AH", "2S", "6S"]

# for i in range(len(a[:5])):
#     for element in list(combinations_with_replacement(a[:5], i)):
#         print(element)

# stuff = [1, 2, 3]
# de_stuff = [4, 5, 6]
# for L in range(1, len(stuff)+1):
#     for subset in combinations(range(len(stuff)), L):
#         subset = stuff[:]
#         for counter,
#         print(subset)

import itertools
#a = ["1", "2", "3", "4", "5", "6"]
permut = set(a)


def getAllKombos(stuff):
    returnvalue = set()
    for L in range(0, len(stuff) + 1):
        for subset in itertools.permutations(stuff, L):
            for i in subset:
                x = x + (str(i))
                if len(x) == 3:
                    returnvalue.add(x)
            x = ""
    return returnvalue

print(getAllKombos(permut).__len__())

# for i in range(1, len(player) + 1):
#     for combs in combinations(range(len(player)), i):
#         combs = combs[:]
#         for counter, rep in enumerate(combs):
#             combs[counter] = deck[counter]
#         total_hands.append(combs)


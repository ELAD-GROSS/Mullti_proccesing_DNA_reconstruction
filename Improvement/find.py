import random
from Improvement.Utilities import *

def possible_rotation(a):
    lst = []
    b = len(a)
    for i in range(b):
        c = a[i:] + a[:i]
        lst.append(c)
    return lst

def find_longest_aux(possible1, possible2):
    if (len(possible1) >= 10):
        print(len(possible1), end=" :")
        print(possible1)
        exit(0)
    """
    :param possible1: classifications already used
    :param possible2: set of all Illegal, for example if we have [...,AC,AT,...] so AC->CT we can't use CT->TA,TA->AC
    :return: maximum list of legal classifications
    """
    maximum = dict()
    for letter in ['A', 'C', 'G', 'T']:
        flag = False

        if (possible1[-1][1:] + letter) in possible1:
            flag = True
            maximum[letter] = possible1

        s = possible1[-1] + letter
        rotations = possible_rotation(s)
        for rotation in rotations:
            if rotation in possible2:
                flag = True
                maximum[letter] = possible1

        if not flag:

            possible1_new = possible1.copy()
            possible1_new.append(possible1[-1][1:] + letter)

            possible2_new = possible2.copy()
            for rotation in rotations:
                possible2_new.add(rotation)

            maximum[letter] = find_longest_aux(possible1_new, possible2_new)

    lst_ret = []
    for val in maximum.values():
        if len(lst_ret) < len(val):
            lst_ret = val
    return lst_ret


def find_longest(letters_amount):
    if letters_amount in longest_seq_by_letters_amount:
        return longest_seq_by_letters_amount[letters_amount]
    start = ""
    letters = ['A', 'C', 'G', 'T']
    for i in range(letters_amount):
        start += letters[i % 4]
    return find_longest_aux([start], set())

def is_good(lst):
    s_1 = set()
    flag_1 = True
    for element_1 in lst:
        if element_1 in s_1:
            flag_1 = False
        s_1.add(element_1)
    set_new = set()
    for i in range(len(lst) - 1):
        st_1 = lst[i] + lst[i + 1][1:]
        r = possible_rotation(st_1)
        for r in set_new:
            if r in set_new:
                return False
            set_new.add(r)
    return True


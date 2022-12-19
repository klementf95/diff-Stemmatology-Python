#!/usr/bin/env python

import re
import sys
from typing import List, Tuple

from Algorithm.Diff.lib import Algorithm_Diff

# Debug level CHANGE
# 0 : only matrix
# 1 : .. and a list of pot. leitfehler (lf) and their score
# 2 : ..... and a list of pot. lf and the ms. the occur in
# 3 : ....... and a list of matches of pot. lf
debug = 1

cut = 0  # threshold for globalLeit, currently not used
weight = 20  # weight. lf are counted .-times more for the best of them, the others proportionally down to 1

scoremax = 1
ur = {}
score = {}
mss_hash = {}
ms_label_array = []

# standardisation
num_of_mss = 0
for line in sys.stdin:
    line = line.rstrip()

    line = re.sub(r"[\,!\?\"]", "", line)  # remove punctuation
    # line = re.sub(r"\.", " ", line)  # remove . ?
    line = re.sub(r"\s[^\s]*\*[^\s]*", " €", line)  # convert word with a *-wildcard to €
    line = re.sub(r"\s+$", "", line)

    # label manuscripts (3 chars), or n chars make (n-1) dots in next line
    if re.match(r"^(\w..)[\w\s]{7}(.+)$", line):
        mss_hash["       " + r"$1"] = r"$2"  # hash of all mss.
        ms_label_array[num_of_mss] = "       " + r"$1"  # all mss. label, n: index

        mss_hash[ms_label_array[num_of_mss]] = re.sub(r"\([^\)]+\)", "", mss_hash[ms_label_array[num_of_mss]])  # remove ()
        mss_hash[ms_label_array[num_of_mss]] = re.sub(r"\[[^\]]+\]", "", mss_hash[ms_label_array[num_of_mss]])  # remove []

        num_of_mss += 1

wlist()
# remove to get a fast result without calculating the lff

##########

print(len(ms_label_array))  # print length of array
print("\n" + ms_label_array[0] + "\n")

for ms_index in range(1, len(ms_label_array)):
    print(ms_label_array[ms_index])
    for other_ms_index in range(ms_index):
        word_array_ms1 = mss_hash[ms_label_array[ms_index]].split(" ")  # split content of this ms into words
        word_array_ms2 = mss_hash[ms_label_array[other_ms_index]

        # diff computes the smallest set of additions and deletions necessary to turn the first sequence into the second
        # and returns a 2-dim array of differences (hunks with sequences); 
        # each difference is a list of 3 elements (-/+, position of the change, string), e.g.:
        # [ 
        #   [ 
        #      [ '-', 0, 'a' ] 
        #      [ '+', 0, 'b' ] 
        #   ], 
        #   [ 
        #      [ '-', 5, 'c' ] 
        #      [ '+', 5, 'd' ] 
        #   ] 
        # ]
        diff = Algorithm_Diff.diff(word_array_ms1, word_array_ms2)

        # sdiff returns a list of string with -/+. It is faster than diff.
        sdiff = Algorithm_Diff.sdiff(word_array_ms1, word_array_ms2)

        # Get the longest common subsequence
        lcs = Algorithm_Diff.LCS(word_array_ms1, word_array_ms2)

        # traverse_sequences traverses two input sequences in parallel and returns a list of 3-element lists (a, b, action).
        # a is an element from the first sequence, b is an element from the second sequence, and action is one of the
        # following:
        #  'u' Both elements are present and equal.
        #  'c' Both elements are present and different.
        #  '-' Element a is present but element b is not.
        #  '+' Element b is present but element a is not.
        traverse_sequences = Algorithm_Diff.traverse_sequences(word_array_ms1, word_array_ms2, lambda x: x[0])

        # traverse_balanced traverses two input sequences and returns a list of 3-element lists (a, b, action).
        # a is an element from the first sequence, b is an element from the second sequence, and action is one of the
        # following:
        #  'u' Both elements are present and equal.
        #  'c' Both elements are present and different.
        #  '-' Element a is present but element b is not.
        #  '+' Element b is present but element a is not.
        traverse_balanced = Algorithm_Diff.traverse_balanced(word_array_ms1, word_array_ms2, lambda x: x[0])

        # calculate leitfehler (lf)
        leitfehler(diff, sdiff, lcs, traverse_sequences, traverse_balanced)

        # print result
        print(" " + str(el) + " ")
        # matrix.assign(ms_index + 1, other_ms_index + 1, el)
        # matrix.assign(other_ms_index + 1, ms_index + 1, el)

        # diff computes the smallest set of additions and deletions necessary to turn the first sequence into the second
        # and returns a 2-dim array of differences (hunks with sequences); 
        # each difference is a list of 3 elements (-/+, position of the change, string), e.g.:
        # [ 
        #   [ 
        #      [ '-', 0, 'a' ] 
        #      [ '+', 0, 'b' ] 
        #   ], 
        #   [ 
        #      [ '-', 5, 'c' ] 
        #      [ '+', 5, 'd' ] 
        #   ] 
        # ]
        diff = Algorithm_Diff.diff(word_array_ms1, word_array_ms2)

        # sdiff returns a list of string with -/+. It is faster than diff.
        sdiff = Algorithm_Diff.sdiff(word_array_ms1, word_array_ms2)

        # Get the longest common subsequence
        lcs = Algorithm_Diff.LCS(word_array_ms1, word_array_ms2)

        # traverse_sequences traverses two input sequences in parallel and returns a list of 3-element lists (a, b, action).
        # a is an element from the first sequence, b is an element from the second sequence, and action is one of the
        # following:
        #  'u' Both elements are present and equal.
        #  'c' Both elements are present and different.
        #  '-' Element a is present but element b is not.
        #  '+' Element b is present but element a is not.
        traverse_sequences = Algorithm_Diff.traverse_sequences(word_array_ms1, word_array_ms2, lambda x: x[0])

        # traverse_balanced traverses two input sequences and returns a list of 3-element lists (a, b, action).
        # a is an element from the first sequence, b is an element from the second sequence, and action is one of the
        # following:
        #  'u' Both elements are present and equal.
        #  'c' Both elements are present and different.
        #  '-' Element a is present but element b is not.
        #  '+' Element b is present but element a is not.
        traverse_balanced = Algorithm_Diff.traverse_balanced(word_array_ms1, word_array_ms2, lambda x: x[0])

        # calculate leitfehler (lf)
        leitfehler(diff, sdiff, lcs, traverse_sequences, traverse_balanced)

        # print result
        print(" " + str(el) + " ")
        # matrix.assign(ms_index + 1, other_ms_index + 1, el)
        # matrix.assign(other_ms_index + 1, ms_index + 1, el)

def leitfehler(diff, sdiff, lcs, traverse_sequences, traverse_balanced):
    global scoremax, weight, ur, score

    best_lf_count = 0
    best_lf = ""
    best_ms = ""
    second_best_lf_count = 0
    second_best_lf = ""
    second_best_ms = ""

    # Calculate the leitfehler for each hunk in the diff
    for hunk in diff:
        if debug > 2:
            print(hunk)

        for item in hunk:
            if item[0] == "-" or item[0] == "+":
                if debug > 2:
                    print(item)

                # Check if this leitfehler has already been seen
                if item[2] in ur:
                    if debug > 2:
                        print(item[2])

                    # Increment the count for this leitfehler
                    ur[item[2]] += 1
                else:
                    # This is a new leitfehler, so set its count to 1
                    ur[item[2]] = 1

                # Calculate the score for this leitfehler
                lf_score = weight * (1 - ur[item[2]] / scoremax) + 1
                if lf_score < 1:
                    lf_score = 1

                # Check if this is the best leitfehler so far
                if lf_score > best_lf_count:
                    second_best_lf_count = best_lf_count
                    second_best_lf = best_lf
                    second_best_ms = best_ms
                    best_lf_count = lf_score
                    best_lf = item[2]
                    best_ms = item[0]
                elif lf_score > second_best_lf_count:
                    second_best_lf_count = lf_score
                    second_best_lf = item[2]
                    second_best_ms = item[0]

    # Calculate the global leitfehler score
    global_lf_score = 0
    if best_lf_count > 0:
        global_lf_score = best_lf_count + second_best_lf_count / 2

    if debug > 0:
        print("best_lf_count: " + str(best_lf_count))
        print("best_lf: " + best_lf)
        print("best_ms: " + best_ms)
        print("second_best_lf_count: " + str(second_best_lf_count))
        print("second_best_lf: " + second_best_lf)
        print("second_best_ms: " + second_best_ms)
        print("global_lf_score: " + str(global_lf_score))

    # Save the scores for this pair of manuscripts
    score[ms_label_array[ms_index] + ms_label_array[other_ms_index]] = global_lf_score
    score[ms_label_array[other_ms_index] + ms_label_array[ms_index]] = global_lf_score


# Calculate the leitfehler scores for all pairs of manuscripts
def wlist

def wlist():
    global ur, scoremax, score

    # Calculate the maximum score
    scoremax = len(ms_label_array) * weight

    # Initialize the leitfehler counts and scores
    ur = {}
    score = {}

    # Compare each pair of manuscripts
    for ms_index in range(1, len(ms_label_array)):
        for other_ms_index in range(ms_index):
            word_array_ms1 = mss_hash[ms_label_array[ms_index]].split(" ")  # split content of this ms into words
            word_array_ms2 = mss_hash[ms_label_array[other_ms_index]].split(" ")  # split content of the other ms into words

            # Calculate the leitfehler scores for this pair of manuscripts
            dodiff(word_array_ms1, word_array_ms2)

if __name__ == "__main__":
    # Read the input manuscripts
    read_input()

    # Calculate the leitfehler scores for all pairs of manuscripts
    wlist()



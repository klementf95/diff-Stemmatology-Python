#! /usr/bin/python


#a python version that more closely resembles the perl version syntactically

import sys
import difflib

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
    line = line.strip()  # Chop off the last char

    line = line.translate(str.maketrans("","", ",!?"))  # remove punctuation
    # line = line.replace(".", " ")  # remove . ?
    line = line.replace(" * ", " €")  # convert word with a *-wildcard to €

    # label manuscripts (3 chars), or n chars make (n-1) dots in next line
    if line.startswith("(w..)[w.s]{7}(.+)"):
        mss_hash[f"{line[:3]}       "] = line[7:]  # hash of all mss.
        ms_label_array.append(f"{line[:3]}       ")  # all mss. label, n: index

        mss_hash[ms_label_array[num_of_mss]] = mss_hash[ms_label_array[num_of_mss]].translate(str.maketrans("","", "()"))  # remove  ()
        mss_hash[ms_label_array[num_of_mss]] = mss_hash[ms_label_array[num_of_mss]].translate(str.maketrans("","", "[]"))  # remove  []

        num_of_mss += 1

wlist()
# remove to get a fast result without calculating the lff

print(len(ms_label_array))  # print length of array
print(ms_label_array[0])

for ms_index in range(1, len(ms_label_array)):
    print(ms_label_array[ms_index], end=" ")
   
or other_ms_index in range(ms_index):
        word_array_ms1 = mss_hash[ms_label_array[ms_index]].split()  # split content of this ms into words
        word_array_ms2 = mss_hash[ms_label_array[other_ms_index]].split()  # split content of the other ms into words

        # diff
        el = dodiff(word_array_ms1, word_array_ms2)
        print(el, end=" ")
        # matrix[ms_index+1][other_ms_index+1] = el
        # matrix[other_ms_index+1][ms_index+1] = el

    print()
    

def dodiff(a1, a2):
    # Copy the two arrays passed to this function into the variables word_arr_ms1 and word_arr_ms2
    word_arr_ms1 = a1
    word_arr_ms2 = a2

    # difflib.Differ.compute_diff computes the smallest set of additions and deletions necessary to turn the first sequence into the second
    # and returns a list of differences (hunks with sequences);
    # each difference is a tuple of 3 elements (-/+, position of the change, string), e.g.:
    # [
    #   ("-", 0, "This"),
    #   ("+", 0, "That"),
    #   (" ", 1, "is"),
    #   (" ", 2, "a"),
    #   (" ", 3, "test."),
    # ]
    diffs = list(difflib.Differ().compute_diff(word_arr_ms1, word_arr_ms2))

    leit_hash = {}
    leit_hash_count = {}
    leit_array = []
    leit_hash_all = {}

    for diff in diffs:
        diff_type, index, word = diff
        if diff_type == "-":
            leit_hash[word] = index
            if word in leit_hash_count:
                leit_hash_count[word] += 1
            else:
                leit_hash_count[word] = 1
        elif diff_type == "+":
            leit_hash[word] = index
            if word in leit_hash_count:
                leit_hash_count[word] += 1
            else:
                leit_hash_count[word] = 1
        elif diff_type == " ":
            if word in leit_hash_count:
                del leit_hash_count[word]
                del leit_hash[word]

    for key in leit_hash_count.keys():
        leit_array.append((leit_hash[key], key))

    leit_array = sorted(leit_array)

    globalLeit = 0
    for i in range(len(leit_array)):
        leit_hash_all[leit_array[i][1]] = (
            leit_array[i][0],
            leit_hash_count[leit_array[i][1]],
        )
        globalLeit += leit_hash_count[leit_array[i][1]]

    if debug > 2:
        for i in range(len(leit_array)):
            print(f"{leit_array[i][1]}: {leit_hash_count[leit_array[i][1]]}")

    return globalLeit

def wlist():
    globalLeit = 0
    for i in range(len(leit_array)):
        globalLeit += leit_hash_count[leit_array[i][1]]

    if debug > 0:
        print(f"GlobalLeit: {globalLeit}")

    if debug > 1:
        for i in range(len(leit_array)):
            print(f"{leit_array[i][1]}: {leit_hash_count[leit_array[i][1]]}")

    if debug > 2:
        for i in range(len(leit_array)):
            print(f"{leit_array[i][1]}: {leit_hash_count[leit_array[i][1]]}")

if debug > 3:
    for i in range(len(leit_array)):
        for j in range(len(leit_array)):
            if leit_array[i][1] == leit_array[j][1]:
                print(f"{leit_array[i][1]} : {leit_array[i][0]} - {leit_array[j][0]}")

scoremax = 1
for i in range(len(leit_array)):
    if leit_hash_count[leit_array[i][1]] == max(leit_hash_count.values()):
        score[leit_array[i][1]] = weight
    else:
        score[leit_array[i][1]] = (
            leit_hash_count[leit_array[i][1]]
            * weight
            // max(leit_hash_count.values())
        )
    if score[leit_array[i][1]] > scoremax:
        scoremax = score[leit_array[i][1]]

for i in range(len(leit_array)):
    if score[leit_array[i][1]] == scoremax:
        score[leit_array[i][1]] = weight
    else:
        score[leit_array[i][1]] = score[leit_array[i][1]] * weight // scoremax
        
    
    ur = {}
for i in range(len(leit_array)):
    ur[leit_array[i][1]] = leit_hash_count[leit_array[i][1]]

ur = sorted(ur.items(), key=lambda item: item[1])

if debug > 0:
    print(f"GlobalLeit: {globalLeit}")

if debug > 1:
    for i in range(len(ur)):
        print(f"{ur[i][0]}: {ur[i][1]}")

if debug > 2:
    for i in range(len(ur)):
        print(f"{ur[i][0]}: {ur[i][1]}")

if debug > 3:
    for i in range(len(ur)):
        for j in range(len(ur)):
            if ur[i][0] == ur[j][0]:
                print(f"{ur[i][0]} : {leit_hash_all[ur[i][0]][0]} - {leit_hash_all[ur[j][0]][0]}")

print()
print("Leitfehler-Matrix:")
print()

matrix = []
for i in range(num_of_mss):
    matrix.append([0] * num_of_mss)

for ms_index in range(1, num_of_mss):
    for other_ms_index in range(ms_index):
        word_array_ms1 = mss_hash[ms_label_array[ms_index]].split()  # split content of this ms into words
        word_array_ms2 = mss_hash[ms_label_array[other_ms_index]].split()  # split content of the other ms into words

        # diff
        el = dodiff(word_array_ms1, word_array_ms2)
        matrix[ms_index][other_ms_index] = el
        matrix[other_ms_index][ms_index] = el

for i in range(num_of_mss):
    print(f"{ms_label_array[i]}: {matrix[i]}")

print()
print("Leitfehler-Matrix mit Gewichtung:")
print()

matrix_weighted = []
for i in range(num_of_mss):
    matrix_weighted.append([0] * num_of_mss)

for ms_index in range(1, num_of_mss):
    for other_ms_index in range(ms_index):
        word_array_ms1 = mss_hash[ms_label_array[ms_index]].split()  # split content of this ms into words
        word_array_ms2 = mss_hash[ms_label_array[other_ms_index]].split()  # split content of the other ms into words

        # diff
        el = dodiff(word_array_ms1, word_array_ms2)
        matrix_weighted[ms_index][other_ms_index] = el * weight
        matrix_weighted[other_ms_index][ms_index] = el * weight
        
print()
print("Leitfehler-Matrix mit Gewichtung (Prozent):")
print()

matrix_weighted_percent = []
for i in range(num_of_mss):
    matrix_weighted_percent.append([0] * num_of_mss)

for ms_index in range(1, num_of_mss):
    for other_ms_index in range(ms_index):
        word_array_ms1 = mss_hash[ms_label_array[ms_index]].split()  # split content of this ms into words
        word_array_ms2 = mss_hash[ms_label_array[other_ms_index]].split()  # split content of the other ms into words

        # diff
        el = dodiff(word_array_ms1, word_array_ms2)
        matrix_weighted_percent[ms_index][other_ms_index] = (
            el * weight * 100 // globalLeit
        )
        matrix_weighted_percent[other_ms_index][ms_index] = (
            el * weight * 100 // globalLeit
        )

for i in range(num_of_mss):
    print(f"{ms_label_array[i]}: {matrix_weighted_percent[i]}")
    
    
    print()
print("Leitfehler-Matrix mit Gewichtung (Prozent) sortiert:")
print()

matrix_weighted_percent_sorted = []
for i in range(num_of_mss):
    matrix_weighted_percent_sorted.append([0] * num_of_mss)

for ms_index in range(1, num_of_mss):
    for other_ms_index in range(ms_index):
        word_array_ms1 = mss_hash[ms_label_array[ms_index]].split()  # split content of this ms into words
        word_array_ms2 = mss_hash[ms_label_array[other_ms_index]].split()  # split content of the other ms into words

        # diff
        el = dodiff(word_array_ms1, word_array_ms2)
        matrix_weighted_percent_sorted[ms_index][other_ms_index] = (
            el * weight * 100 // globalLeit
        )
        matrix_weighted_percent_sorted[other_ms_index][ms_index] = (
            el * weight * 100 // globalLeit
        )

matrix_weighted_percent_sorted = sorted(
    matrix_weighted_percent_sorted, key=lambda row: sum(row), reverse=True
)

for row in matrix_weighted_percent_sorted:
    print(row)

print()
print("Leitfehler-Matrix mit Gewichtung (Prozent) sortiert (absolut):")
print()

matrix_weighted_percent_sorted_abs = []
for i in range(num_of_mss):
    matrix_weighted_percent_sorted_abs.append([0] * num_of_mss)

for ms_index in range(1, num_of_mss):
    for other_ms_index in range(ms_index):
        word_array_ms1 = mss_hash[ms_label_array[ms_index]].split()  # split content of this ms into words
        word_array_ms2 = mss_hash[ms_label_array[other_ms_index]].split()  # split content of the other ms into words

        # diff
        el = dodiff(word_array_ms1, word_array_ms2)
        matrix_weighted_percent[ms_index][other_ms_index] = (
            el * weight * 100 // globalLeit
        )
        matrix_weighted_percent[other_ms_index][ms_index] = (
            el * weight * 100 // globalLeit
        )

for i in range(num_of_mss):
    print(f"{ms_label_array[i]}: {matrix_weighted_percent[i]}")

print()
print("Leitfehler-Matrix mit Gewichtung (Prozent) sortiert:")
print()

matrix_weighted_percent_sorted = []
for i in range(num_of_mss):
    matrix_weighted_percent_sorted.append([0] * num_of_mss)

for ms_index in range(1, num_of_mss):
    for other_ms_index in range(ms_index):
        word_array_ms1 = mss_hash[ms_label_array[ms_index]].split()  # split content of this ms into words
        word_array_ms2 = mss_hash[ms_label_array[other_ms_index]].split()  # split content of the other ms into words

        # diff
        el = dodiff(word_array_ms1, word_array_ms2)
        matrix_weighted_percent_sorted[ms_index][other_ms_index] = (
            el * weight * 100 // globalLeit
        )
        matrix_weighted_percent_sorted[other_ms_index][ms_index] = (
            el * weight * 100 // globalLeit
        )

matrix_weighted_percent_sorted = sorted(
    matrix_weighted_percent_sorted, key=lambda row: sum(row), reverse=True
)

for row in matrix_weighted_percent_sorted:
    print(row)

print()
print("Leitfehler-Matrix mit Gewichtung (Prozent) sortiert (absolut):")
print()

matrix_weighted_percent_sorted_abs = []
for i in range(num_of_mss):
    matrix_weighted_percent_sorted_abs.append([0] * num_of_mss)

for ms_index in range(1, num_of_mss):
    for other_ms_index in range(ms_index):
        word_array_ms1 = mss_hash[ms_label_array[ms_index]].split()  # split content of this ms into words
        word_array_ms2 = mss_hash[ms_label_array[other_ms_index]].split()  # split content of the other ms into words

        # diff
        el = dodiff(word_array_ms1, word_array_ms2)
        matrix_weighted_percent_sorted_abs[ms_index][other_ms_index] = (
            el * weight // globalLeit
        )
        matrix_weighted_percent_sorted_abs[other_ms_index][ms_index] = (
            el * weight // globalLeit
        )

matrix_weighted_percent_sorted_abs = sorted(
    matrix_weighted_percent_sorted_abs, key=lambda row: sum(row), reverse=True
)

for row in matrix_weighted_percent_sorted_abs:
    print(row)
    
  
  
  
print()
print("Leitfehler-Matrix mit Gewichtung (Prozent) sortiert (absolut) transponiert:")
print()

matrix_weighted_percent_sorted_abs_transposed = []
for i in range(num_of_mss):
    matrix_weighted_percent_sorted_abs_transposed.append([0] * num_of_mss)

for ms_index in range(1, num_of_mss):
    for other_ms_index in range(ms_index):
        word_array_ms1 = mss_hash[ms_label_array[ms_index]].split()  # split content of this ms into words
        word_array_ms2 = mss_hash[ms_label_array[other_ms_index]].split()  # split content of the other ms into words

        # diff
        el = dodiff(word_array_ms1, word_array_ms2)
        matrix_weighted_percent_sorted_abs_transposed[ms_index][other_ms_index] = (
            el * weight // globalLeit
        )
        matrix_weighted_percent_sorted_abs_transposed[other_ms_index][ms_index] = (
            el * weight // globalLeit)

matrix_weighted_percent_sorted_abs_transposed = sorted(
    matrix_weighted_percent_sorted_abs_transposed,
    key=lambda row: sum(row),
    reverse=True,
)

for row in matrix_weighted_percent_sorted_abs_transposed:
    print(row)
    
    
    for ms_index in range(1, num_of_mss):
    print(ms_label_array[ms_index], end=" ")
    for other_ms_index in range(ms_index):
        word_array_ms1 = mss_hash[ms_label_array[ms_index]].split()  # split content of this ms into words
        word_array_ms2 = mss_hash[ms_label_array[other_ms_index]].split()  # split content of the other ms into words

        # diff
        el = dodiff(word_array_ms1, word_array_ms2)
        print(f"{el} ", end="")
    print()

    
  def leitfehler(word_array_ms1, word_array_ms2):
    global ur
    global score
    global debug
    global mss_hash
    global ms_label_array
    global scoremax

    lf = {}
    s = 0
    n = 0
    score = {}
    for i in range(len(word_array_ms1)):
        for j in range(len(word_array_ms2)):
            if (
                (word_array_ms1[i] == word_array_ms2[j])
                and (i not in ur)
                and (j not in ur)
            ):
                if (
                    (i > 0)
                    and (j > 0)
                    and (word_array_ms1[i - 1] == word_array_ms2[j - 1])
                ):
                    s += 1
                    if (
                        (i > 1)
                        and (j > 1)
                        and (word_array_ms1[i - 2] == word_array_ms2[j - 2])
                    ):
                        s += 1
                    n += 1
                elif (
                    (i < len(word_array_ms1) - 1)
                    and (j < len(word_array_ms2) - 1)
                    and (word_array_ms1[i + 1] == word_array_ms2[j + 1])
                ):
                    s += 1
                    if (
                        (i < len(word_array_ms1) - 2)
                        and (j < len(word_array_ms2) - 2)
                        and (word_array_ms1[i + 2] == word_array_ms2[j + 2])
                    ):
                        s += 1
                    n += 1
                else:
                    n += 1
                if (s / n > scoremax):
                    scoremax = s / n
                lf[i] = s / n
                score[i] = s / n
                ur[i] = 1
                ur[j] = 1
                s = 0
                n = 0
    if debug > 2:
        print(score)
    return len(lf)

def wlist():
    global ur
    global score
    global debug
    global mss_hash
    global ms_label_array
    global scoremax

    globalLeit = 0
    for i in range(num_of_mss):
        for j in range(i + 1, num_of_mss):
            word_array_ms1 = mss_hash[ms_label_array[i]].split()  # split content of this ms into words
            word_array_ms
  
    #hier leider abgestürzt
'''This section of code creates a weighted version of the leitfehler matrix in percent, sorted by the sum of the values in each row. It does this by multiplying the values in the matrix by the weight parameter and dividing by the total number of leitfehler (globalLeit). It then sorts the matrix in descending order based on the sum of the values in each row and prints out the sorted matrix.'''

def dodiff(a1, a2):
    wordArrMs1 = a1
    wordArrMs2 = a2

    diffArray = diff(wordArrMs1, wordArrMs2)

    dist = 0
    for hunk in diffArray:
        sequenceArray = hunk
        distInHunk = 0
        for sequence in sequenceArray:
            word = " ".join(sequence)
            word = re.sub(r"^. \d+ (.+)", r"\1", word)
            if score.get(word) and scoremax * weight != 0:
                distInHunk += score[word] / scoremax * weight
            distInHunk += 1
        dist += distInHunk
    return int(dist + 0.5)

msLabelArray = []
mssHash = {}

print(len(msLabelArray))
print(msLabelArray[0])

for msIndex in range(1, len(msLabelArray)):
    print(msLabelArray[msIndex])
    for otherMsIndex in range(0, msIndex):
        wordArrayMs1 = mssHash[msLabelArray[msIndex]].split(" ")
        wordArrayMs2 = mssHash[msLabelArray[otherMsIndex]].split(" ")

        el = dodiff(wordArrayMs1, wordArrayMs2)
        print(" {} ".format(el))
    print("")

def outdiff(a, b):
    arr1 = list(mssHash[a])
    arr2 = list(mssHash[b])

    diffArray = diff(arr1, arr2)

    for i in diffArray:
        print("({}): ".format(len(i)), end="")
        for j in i:
            for k in j:
                print(k, end=",")
        print("")
  ################################################################      
    def dodiff(a1, a2):
    # Copy the two arrays passed to this subroutine into the variables wordArrMs1 and wordArrMs2
    word_arr_ms1 = list(a1)
    word_arr_ms2 = list(a2)

    # diff computes the smallest set of additions and deletions necessary to turn the first sequence into the second
    # and returns a 2-dim array of differences (hunks with sequences); 
    # each difference is a list of 3 elements (-/+, position of the change, string), e.g.:
    # [ 
    #   ['-', 0, 'example'], 
    #   ['+', 1, 'sample']
    # ]
    diffs = difflib.Differ().compare(word_arr_ms1, word_arr_ms2)

    leit_hash = {}
    leit_hash_count = {}
    leit_hash_ms = {}
    leit_array = []
    global_leit = []
    for el in diffs:
        if el[0] == '-' or el[0] == '+':
            leit_hash[el[2]] = 0
            leit_hash_count[el[2]] = 0
            leit_hash_ms[el[2]] = []
            leit_array.append(el[2])
        elif el[0] == ' ':
            if el[2] in leit_hash:
                leit_hash[el[2]] += 1
                leit_hash_count[el[2]] += 1
            else:
                leit_hash[el[2]] = 1
                leit_hash_count[el[2]] = 1
                leit_hash_ms[el[2]] = []
                leit_array.append(el[2])
    leit_array.sort(key=lambda x: leit_hash[x], reverse=True)
    leit_array = leit_array[:min(len(leit_array), 20)]
    leit_array.sort()
    global_leit = list(leit_array)
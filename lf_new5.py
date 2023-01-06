#!/usr/bin/python

import sys
sys.path.append('./Algorithm-Diff-1.201/lib')
import Algorithm.Diff as Diff
import List.Util as Util
import difflib
import re

# Debug level CHANGE
# 0 : only matrix
# 1 : .. and a list of pot. leitfehler (lf) and their score
# 2 : ..... and a list of pot. lf and the ms. the occur in
# 3 : ....... and a list of matches of pot. lf
debug=1

cut=0 # threshold for globalLeit, currently not used
weight=20 # weight. lf are counted .-times more for the best of them, the others proportionally down to 1

scoremax=1
ur={}
score={}
mssHash={}
msLabelArray=[]

# standardisation
numOfMss=0
for inst in sys.stdin:
    inst=inst.strip() # Chop off the last char

    inst=inst.replace(',','').replace('!','').replace('?','').replace('"','') # remove punctuation
    # in=in.replace('.',' ') # remove . ?
    inst=inst.replace(r'\s[^\s]*\*[^\s]*', ' €') # convert word with a *-wildcard to €
    inst=inst.rstrip()

    # label manuscripts (3 chars), or n chars make (n-1) dots in next line
    # Anfang der zeile, mindestens drei zeichen, erstes alpha. gefolgt von min 7 zeichen an text oder white space, gefolgt von zufälliger anzahl an text. 
    if inst.match(r'^(\w..)[\w\s]{7}(.+)$'):
        
        # die nächsten beiden lines sind zu testen, da uns nicht ganz ersichtlich ist, wie sie funktioniert.
        # Vermutung: Zergliederung in eine Siglen und eine Text Variable, die auf ein key/value paar aufgeteilt und abgelegt werden.
        # Variablen + indexierung vermutlich neu zu setzen
        mssHash[f"{1:<8}"]=2
        msLabelArray[numOfMss]=f"{1:<8}" # all mss. label, n: index

        #Reverse engineering bug fixing, überrprufung ob die beiden dicts richtig erstellt wurden und löschen von Klammern
        mssHash[msLabelArray[numOfMss]]=mssHash[msLabelArray[numOfMss]].replace(r'\([^\)]+\)','') # remove  ()
        mssHash[msLabelArray[numOfMss]]=mssHash[msLabelArray[numOfMss]].replace(r'\[[^\]]+\]','') # remove  []

        numOfMss+=1  

#wlist()  # call einer weiter unten definierten Funktion
# remove to get a fast result without calculating the lff

##########

# Output Anfang, möglicher String anzuführen, der eine kurze Erklärung des Outputs liefert.
# Option verbose=False (default)
print(len(msLabelArray)) # print length of array
print(msLabelArray[0]+'\n') # erste zeile

for msIndex in range(1,len(msLabelArray)):
    print(msLabelArray[msIndex])
    # schreib das label in die zeile
    for otherMsIndex in range(0,msIndex):
        # Anzeil der Zeilen mal Spalten (eg. für den aktuellen Text, geh alle zuvor bearbeiteten durch) und mache pro Element/Text:
        wordArrayMs1 = mssHash[msLabelArray[msIndex]].split(' ') # split content of this ms into words
        wordArrayMs2 = mssHash[msLabelArray[otherMsIndex]].split(' ')# split content of the other ms into words


        #Hier wird noch do diff gecalled, wobei der gesamte content eines textes mit dem gesamten des andereren 
        # ausgegegben und mit whitespaces umrahmt wird.
        # (diff
        #my $el=dodiff(\@wordArrayMs1, \@wordArrayMs2);
        #print " ".$el." ";
        #$matrix->assign($msIndex+1,$otherMsIndex+1,$el); 
        #$matrix->assign($otherMsIndex+1,$msIndex+1,$el)); 


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

def wlist():
    global cut
    cut = cut * numOfMss * numOfMss / 2500

    mssWordCountHash = {}
    globalWordCountHash = {}

    for msIndex in mssHash.keys():
        msContent = mssHash[msIndex]
        msContent = re.sub(r"[\s\|]+", " ", msContent)
        while re.match(r"^\s*([^\s]+)", msContent):
            m = re.match(r"^\s*([^\s]+)", msContent)
            word = m.group(1)
            msContent = msContent[m.end():]
            mssWordCountHash[msIndex][word] = mssWordCountHash[msIndex].get(word, 0) + 1
            globalWordCountHash[word] = globalWordCountHash.get(word, 0) + 1

leit = []
globalLeit = {}

for msIndex in range(1, len(msLabelArray)):
    currMsLabel = msLabelArray[msIndex]

    for otherMsIndex in range(0, msIndex):
        otherMsLabel = msLabelArray[otherMsIndex]

        for word in globalWordCountHash.keys():
            if re.match(r"...", word) and abs(mssWordCountHash[currMsLabel][word] - mssWordCountHash[otherMsLabel][word]) > 0 and mssWordCountHash[currMsLabel][word] + mssWordCountHash[otherMsLabel][word] < 2:
                leit[msIndex][otherMsIndex][word] = 1
                globalLeit[word] = globalLeit.get(word, 0) + 1

if debug == 2:
    with open("log2", "w") as log2:
        for word in globalLeit.keys():
            if globalLeit[word] > cut:
                log2.write(f"{word} ({globalLeit[word]}) : ")
                for msIndex in range(1, len(msLabelArray)):
                    currMsLabel = msLabelArray[msIndex]
                    if word in mssWordCountHash[currMsLabel]:
                        m = re.match(r"^[^ ]{1,4}", currMsLabel)
                        log2.write(f"{m.group(0)}:{mssWordCountHash[currMsLabel][word]} ")
                log2.write("\n")

ur = {}

for word in globalLeit.keys():
    if globalLeit[word] > cut:
        for otherWord in globalLeit.keys():
            if globalLeit[otherWord] > cut and word < otherWord:
                tab = [0, 0, 0, 0]

                for msIndex in range(1, len(msLabelArray)):
                    currMsLabel = msLabelArray[msIndex]

                    if word in mssWordCountHash[currMsLabel] and otherWord in mssWordCountHash[currMsLabel]:
                        tab[0] += 1
                    elif word in mssWordCountHash[currMsLabel] and otherWord not in mssWordCountHash[currMsLabel]:
                        tab[1] += 1
                    elif word not in mssWordCountHash[currMsLabel] and otherWord in mssWordCountHash[currMsLabel]:
                        tab[2] += 1
                    else:
                        tab[3] += 1

                if tab[0] == 0 and tab[1] > 0 and tab[2] > 0 and tab[3] > 0:
                    if debug:
                        vierer(tab[1], tab[2], tab[3], tab, word, otherWord)
                    r = rating(tab[1], tab[2], tab[3], word, otherWord)
                    s = ratings(tab[1], tab[2], tab[3], word, otherWord)
                    if r > 1:
                        ur[word] = ur.get(word, 0) + (r -


# Calculate counter: number of occurences of word 
for word in globalLeit:
    counter = 0

    # Iterate over all mss and 
    # count the number of mss that contain word
    for msIndex in range(1, len(msLabelArray)):
        currMsLabel = msLabelArray[msIndex]

        if mssWordCountHash[currMsLabel][word] != 0:
            counter += 1
    
    if counter > numOfMss/2:
        counter = numOfMss - counter

    if globalLeit[word] * counter != 0: # if (globalLeit counter for this word * counter) not 0
        score[word] = ur[word] / counter
    else:
        score[word] = ur[word]

# Calculate scoremax
for word in ur:
    scoremax = max(scoremax, score[word])

# Print %ur if debug=1
# logfile
if debug > 0:
    with open("log", "w") as log:
        for k in sorted(score, key=score.get, reverse=True):
            if ur[k] > 0 and score[k] > scoremax/100:
                log.write(f"{k}  --  {int(score[k])} - {ur[k]} {int(score[k]/scoremax*100)}%\n")

def rating(a1, a2, a3, word, otherWord):
    a = [a1, a2, a3]
    r = min(a)

    return r

def ratings(a1, a2, a3, word, otherWord):
    a = [a1, a2, a3]
    s = len(msLabelArray) - (max(a)) - (min(a))

    return s

def vierer(a1, a2, a3, t0, t1, t2, t3, word, otherWord):
    if debug == 3:
        if t0 != 1 and t1 != 1 and t2 != 1 and t3 != 1:
            print(f"{word}/{otherWord} {t0} {t1} {t2} {t3}")
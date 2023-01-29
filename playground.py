#!/usr/bin/python

import re
from collections import defaultdict
import argparse
from argparse import RawTextHelpFormatter
import csv

  
# defining parameters (user input)
# parser = argparse.ArgumentParser(
#     prog = 'Leitfehler Detection',
#     description= 'A Python Script for detecting Leitfehlers from a given text collation. The leitfehlers are pasted into a separate text document named "leitfehler_list.txt". Additionally it produces a lower-triangular distance matrix which can then be further used as input for PHYLIP and its various functionalities.\nThe script starts by reading in the input, which consists of tabular data (in either .csv or .txt format) with its columns  containing labels for the manuscripts followed by a line for every word in each manuscript. The script standardises the input by removing punctuation, it also stores the labels and contents of the manuscripts. Optionally the user can provide the script also with a file of regex or other substitution terms which are then parsed through the preprocessing pipeline as an additional step.\nThe function called dodiff takes two arrays of words in an input and returns the numeric difference between the two arrays. For this it compares the contents of each manuscript to the contents of every other manuscript that precedes it in the array.\nThe actual leitfehler calculation is done by counting the number of times each word appears in each manuscript and comparing these counts between pairs of manuscripts.\nThe script calculates a score for each word in the manuscripts based on the number of manuscripts in which it appears and its global frequency in the manuscripts.',
#     epilog='Authorship: The original Perl version lf_new4 was written by Dieter Bachmann Philipp, Roelli & Eva Sediki. The lf_new5 was rewritten, optimised and translated into Python by Florian Klement & David Siegl.', formatter_class=RawTextHelpFormatter)

# parser.add_argument('-f', '--file', dest='file', required=True, type=str, help='Required: Filepath for the text collation, expects tabular data format (.csv or .txt)')
# parser.add_argument('-c', '--cut', dest='cut', action='store', type=int, default=0, help='Optional: cut off threshold for leitfehler detection score(effective range between 400 and 600)')
# parser.add_argument('-d', '--debug', dest='debug', action='store', type=int, default=1, choices=[0,1], help='Optional: Binary indicator 0 : only matrix 1 : and a list of pot. leitfehler (lf) and their score')
# parser.add_argument('-delim', '--delimiter', dest='delimiter', action='store', type=str, default=',', help='Optional: Delimiter of input file (default: comma)')
# parser.add_argument('-e', '--encoding', dest='encoding', action='store', type=str, default='utf-8', help='Optional: Encoding of input file (default: utf-8) See other available options for function open()')
# parser.add_argument('-r', '--regex', dest='regex', type=str, default = 0, help='Optional: Filepath to a textfile for additional regex patterns to be substituted within the texts, expects the format: every substitution expression consisting of two lines where\nfirst line = matching pattern\nsecond line = substitution pattern')
# parser.add_argument('-w', '--weight', dest='weight', type=float, default = 20, help='Optional: weight. lf are counted .-times more for the best of them, the others proportionally down to 1')
# parser.add_argument('-sm', '--scoremax', dest='scoremax', type=int, default = 1, help='Optional: weighing for probability of leitfehler detection')
# parser.add_argument('-v', '--verbose_vote', dest='verbose_vote', action='store', type=int, default=0, choices=[0,1], help='Optional: Binary indicator 0 : only normal leitfehler list 1 : and a leitfehler list with relevance for each stemma')

# args = parser.parse_args()

# cut = args.cut
# debug = args.debug
# delimiter = args.delimiter
# encoding = args.encoding
# regex = args.regex
# weight = args.weight
# scoremax = args.scoremax
# verbose_vote = args.verbose_vote

mssDict = defaultdict(str)
msLabelArray = []
numOfMss = 0
score = defaultdict(int)
mssWordCountDict = defaultdict(dict)
globalWordCountDict = defaultdict(dict)
leit = []
globalLeit = defaultdict(int)
ur = defaultdict(int)
mssDictList = defaultdict(list)
mssListTemp = []

cut = 0
debug = 1
delimiter = '\t'
encoding = 'ISO-8859-15'
regex = 0
weight = 20
scoremax = 1
verbose_vote = 0



def rating(a1, a2, a3, word, otherWord):
    a = [a1, a2, a3]
    r = min(a)

    return r

def ratings(a1, a2, a3, word, otherWord):
    a = [a1, a2, a3]
    s = len(msLabelArray) - max(a) - min(a)

    return s


with open('./test_data/parzival_aligned.csv','r', newline='', encoding=encoding) as f:
    reader = csv.DictReader(f, delimiter=delimiter, quoting=csv.QUOTE_NONE)
    for label in reader.fieldnames:
        f.seek(0)
        for inst in reader:
            mssListTemp.append(inst[label])
        mssDictList[label.ljust(9)] = mssListTemp.copy()
        mssListTemp.clear()
print(mssDictList)

def diff(list_text1, list_text2):
    temp_diff = []
    for item1, item2 in zip(list_text1, list_text2):
        if item1 != item2:
            if item1 is not None and item1 != '':
                temp_diff.append(item1)
            if item2 is not None and item2 != '':
                temp_diff.append(item2)
    return temp_diff

def dodiff(a1, a2):
    wordArrMs1 = a1
    wordArrMs2 = a2

    diffArray = diff(wordArrMs1, wordArrMs2)
    dist = 0
    for hunk in diffArray:
        sequenceArray = hunk
        distInHunk = 0
        for word in sequenceArray:
            if score[word] and scoremax * weight != 0:
                distInHunk += score[word] / scoremax * weight
            distInHunk += 1
        dist += distInHunk
    return int(dist + 0.5)


msLabelArray = list(mssDictList.keys())
numOfMss = print(len(msLabelArray))
            
    
for key in mssDictList:
    ms = mssDictList[key][1:]
    if ms and ms[-1] == ' ':
        ms = ms[:-1]
    ms = [word.translate(str.maketrans('', '', ',!?"\r\n.()[]:')) for word in ms]
    mssDictList[key] = ms
    if regex != 0:
        with open(regex) as f:
            count = 0
            pattern = []
            repl = []
            for inst in f:
                if count % 2 == 0:
                    pattern.append(inst)
                else:
                    repl.append(inst)
                count += 1
        regexDict = dict(zip(pattern,repl))
        for pat, rep in regexDict.items():
            ms = [re.sub(pat.replace("\n", ""), rep, word) for word in ms]
            mssDictList[key] = ms
    mssDict[key] = "".join(mssDictList[key])
    ms = [word.replace(' ','') for word in ms]
    mssDictList[key] = ms
              

cut = cut * numOfMss * numOfMss / 2500

    
for msIndex in mssDict.keys():
    msContent = mssDict.get(msIndex)
    msContent = re.sub(r"[\s\|]+", " ", msContent)
    while re.match(r"^\s*([^\s]+)", msContent): # while another text can be found in $msContent
        m = re.match(r"^\s*([^\s]+)", msContent)
        word = m.group(1)
        msContent = msContent[m.end():]
        # increment counter for the word found in the ms specific word 
        # mapping and in the global word mapping       
        # mssWordCountDict = {text:{word:count},
        #                         {word:count},
        #                     text:{word:count}
        #                         {word:count}}
        # globalWordCountDict= {{word:count},
        #                     {word:count},
        #                     {word:count},
        #                     {word:count}}
                                              
        mssWordCountDict[msIndex][word] = mssWordCountDict[msIndex].get(word, 0) + 1
        globalWordCountDict[word] = globalWordCountDict.get(word, 0) + 1

    
    
    
    # Hash map over all words in the mss; the keys of the dict are words, 
    # and the value is a counter: how often the word is a leitfehler candidate over all mss


    # finding candidates for leitfehler

        # Matrix of mss that contains a dict; the keys of the dict are words
        # and the value is a bool: 1=is a leitfehler candidate, 0=is not a leitfehler candidate

        # Wörter die insgesamt weniger als zweimal innerhalb von zwei verglichenen Manuskripten vorkommen und hierbei in beiden nicht gleich oft, 
        # werden als Kandidaten herangezogen.
        # Hierbei werden zwei Counter bespielt, ein globaler und einer für jede spezische Manuskript kombination, 
        # um in einer Abstimmung zur Eingnung von Termen zum Schluss zu dienen.
        # Paare an Leitfehler, die nur in wenigen Texten vorkommen, werden höher bewertet.



    
for msIndex in range(1, len(msLabelArray)):
    currMsLabel = msLabelArray[msIndex]
    for otherMsIndex in range(0, msIndex):
        otherMsLabel = msLabelArray[otherMsIndex]
        for word in globalWordCountDict.keys(): 
            #only words with at least 3 characters are considered
            # wenn die Anzahl der Vorkommnisse des Wortes innerhalb der beiden verglichenen Texte abweicht
            # UND die Anzahl der Vorkommnisse des Wortes innerhalb der beiden verglichenen Texte insgesamt geringer als 2 ist.
                if re.match(r"...", word) and abs(mssWordCountDict[currMsLabel].get(word, 0) - mssWordCountDict[otherMsLabel].get(word, 0)) > 0 and mssWordCountDict[currMsLabel].get(word, 0) + mssWordCountDict[otherMsLabel].get(word, 0) < 2:
                    globalLeit[word] = globalLeit.get(word, 0) + 1
                    
if verbose_vote == 1:
    with open("leitfehler_vote.txt", "w") as log2_file:
        for word in globalLeit.keys():
            if globalLeit[word] > cut:
                log2_file.write(f"{word} ({globalLeit[word]}) : ")
                for msIndex in range(1, len(msLabelArray)):
                    currMsLabel = msLabelArray[msIndex]
                    if word in mssWordCountDict[currMsLabel]:
                        currMsLabel_first_4 = currMsLabel[:4]
                        log2_file.write(f"{currMsLabel_first_4.strip()}:{mssWordCountDict[currMsLabel][word]} ")
                log2_file.write("\n")
          
    


for word in globalLeit.keys():
    if globalLeit[word] > cut: 
        for otherWord in globalLeit.keys():
            if globalLeit[otherWord] > cut and word < otherWord:
                tab = [0, 0, 0, 0]
                for msIndex in range(1, len(msLabelArray)):
                    currMsLabel = msLabelArray[msIndex]
                    # für jeden Index in einer Iteration der Label, speicher jedes Label in eine temp variable, 
                    # um durch die Texte zu iterieren und sie zu vergleichen
                    # Both, word and otherWord are in the current ms
                    if word in mssWordCountDict[currMsLabel] and otherWord in mssWordCountDict[currMsLabel]:
                        tab[0] += 1
                    #Eine reihe an vergleichen wird aufgestellt:
                    #Wort1 und Wort2 weeden daraufhin verglichen, ob eines der beiden, beide oder keines in einem manuskript 
                    #enthalten ist oder nicht
                    # Only word is in the the current ms
                    elif word in mssWordCountDict[currMsLabel] and otherWord not in mssWordCountDict[currMsLabel]:
                        tab[1] += 1
                    # Only otherWord is in the the current ms
                    elif word not in mssWordCountDict[currMsLabel] and otherWord in mssWordCountDict[currMsLabel]:
                        tab[2] += 1
                    # Neither word nor otherWord are in the the current ms
                    else:
                        tab[3] += 1

                if tab[0] == 0 and tab[1] > 0 and tab[2] > 0 and tab[3] > 0:
                    r = rating(tab[1], tab[2], tab[3], word, otherWord)
                    s = ratings(tab[1], tab[2], tab[3], word, otherWord)
                    if r > 1:
                        ur[word] = ur[word] + (r - 1) ** 2 * s
                        ur[otherWord] = ur[otherWord] + (r - 1) ** 2 * s
                elif tab[1] == 0 and tab[0] > 0 and tab[2] > 0 and tab[3] > 0:
                    r = rating(tab[0], tab[2], tab[3], word, otherWord)
                    s = ratings(tab[0], tab[2], tab[3], word, otherWord)
                    if r > 1:
                        ur[word] = ur[word] + (r - 1) ** 2 * s
                        ur[otherWord] = ur[otherWord] + (r - 1) ** 2 * s
                elif tab[2] == 0 and tab[0] > 0 and tab[1] > 0 and tab[3] > 0:
                    r = rating(tab[0], tab[1], tab[3], word, otherWord)
                    s = ratings(tab[0], tab[1], tab[3], word, otherWord)
                    if r > 1:
                        ur[word] = ur[word] + (r - 1) ** 2 * s
                        ur[otherWord] = ur[otherWord] + (r - 1) ** 2 * s
                elif tab[3] == 0 and tab[0] > 0 and tab[1] > 0 and tab[2] > 0:
                    r = rating(tab[0], tab[1], tab[2], word, otherWord)
                    s = ratings(tab[0], tab[1], tab[2], word, otherWord)
                    if r > 1:
                        ur[word] = ur[word] + (r - 1) ** 2 * s
                        ur[otherWord] = ur[otherWord] + (r - 1) ** 2 * s

#Counter/Nr. of occurences ist unabhängig von der Matrix zuvor, das relationale Auftreten von einem Wort
# im Verhältnis zu anderen steht nicht mit dem absoluten im Konflikt.

# Calculate counter: number of occurences of word 
for word in globalLeit.keys():
    counter = 0
    for msIndex in range(1, len(msLabelArray)):
        currMsLabel = msLabelArray[msIndex]
        if mssWordCountDict[currMsLabel].get(word, 0) != 0:
            counter += 1   
    if counter > numOfMss/2:
        counter = numOfMss - counter
    
    #Wenn das Wort häufiger als in jedem zweiten Text vorkommt, 
    #dann reduzier den Wert um die Anzahl der texte.
    
    #ur, which stores the scores for each leitfehler candidate,
    #the scores in ur are then normalized by dividing them by the number of occurrences of
    #each leitfehler candidate in the manuscripts, and the resulting values are stored in a 
    #dict called %score (?)

    if globalLeit[word] * counter != 0: # if (globalLeit counter for this word * counter) not 0
        score[word] = ur[word] / counter
    else:
        score[word] = ur[word]

# Calculate scoremax
for word in ur:
    scoremax = max(scoremax, score[word])
    
#Scoremax ist eine Art unsichtbare Hand für die Listung von scorewerten        

print(len(msLabelArray)) # print length of array
print(msLabelArray[0]) # erste zeile


for msIndex in range(1,len(msLabelArray)):
    current_key = msLabelArray[msIndex]
    print(current_key, end='')
    for otherMsIndex in range(0,msIndex):      
        wordArrayMs1 = mssDictList[msLabelArray[msIndex]]
        wordArrayMs2 = mssDictList[msLabelArray[otherMsIndex]]
        el = dodiff(wordArrayMs1, wordArrayMs2)
        print(" {} ".format(el), end='') 
    print()

if debug == 1:
    with open("leitfehler_list.txt", "w") as log:
        for k in sorted(score, key=lambda x: score[x], reverse=True):
            if ur[k] > 0 and score[k] > scoremax/100:
                log.write(f"{k}  --  {int(score[k])} - {ur[k]} {int(score[k]/scoremax*100)}%\n")
                
# print ins log file pro zeile:
# score (normiert) , ur wert (leitfehlerwert) und den score normiert durch scoremax als prozentsatz der wslkeit.


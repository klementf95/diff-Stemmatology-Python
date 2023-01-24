#!/usr/bin/python

import re
import string # noch checken
from collections import defaultdict
import argparse
  
# defining parameters (user input)
parser = argparse.ArgumentParser(
    prog = 'Leitfehler Detection',
    description= 'A Python Script for detecting Leitfehlers from a given text collation.',
    epilog='Authorship: The original Perl version lf_new4 was written by Dieter Bachmann Philipp, Roelli & Eva Sediki. The lf_new5 was rewritten, optimised and translated into Python by Florian Klement & David Siegl.')

parser.add_argument('-f', '--file', dest='file', required=True, help='Filepath for the text collation')
parser.add_argument('-c', '--cut', dest='cut', action='store', type=int, default=0, help='cut off threshold for leitfehler detection')
parser.add_argument('-d', '--debug', dest='debug', action='store', type=int, default=1, choices=[0,1], help='Binary indicator 0 : only matrix 1 : and a list of pot. leitfehler (lf) and their score')

args = parser.parse_args()

cut = args.cut
debug = args.debug

weight = 20 # weight. lf are counted .-times more for the best of them, the others proportionally down to 1

scoremax = 1
mssDict = {}
msLabelArray = []
numOfMss = 0
score = defaultdict(int)
mssWordCountDict = defaultdict(dict)
globalWordCountDict = defaultdict(dict)
leit = []
globalLeit = defaultdict(int)
ur = defaultdict(int)

#the main part of the script calculates a score for each word in the manuscripts based
# on the number of manuscripts in which it appears and its global frequency
# in the manuscripts. It also calculates a scoremax value, which is the maximum score among all the words.


def rating(a1, a2, a3, word, otherWord):
    a = [a1, a2, a3]
    r = min(a)

    return r

def ratings(a1, a2, a3, word, otherWord):
    a = [a1, a2, a3]
    s = len(msLabelArray) - max(a) - min(a)

    return s


# Vierer wird in der aktuellen Variante nicht verwendet, da der Fall debug = 3 nicht im Einsatz ist.

def vierer(t0, t1, t2, t3, word, otherWord):
    if debug == 3:
        if t0 != 1 and t1 != 1 and t2 != 1 and t3 != 1:
            print(f"{word}/{otherWord} {t0} {t1} {t2} {t3}")

        
# standardisation        
#for inst in fileinput.input():
with open(args.file) as f:
    for inst in f:
        inst=inst.strip() # Chop off the last char
        inst=inst.replace(',','').replace('!','').replace('?','').replace('"','').replace('.',' ') # remove punctuation
        inst=inst.replace(r'\s[^\s]*\*[^\s]*', ' €') # convert word with a *-wildcard to €
        inst=inst.rstrip()
        # label manuscripts (3 chars), or n chars make (n-1) dots in next line
        # Anfang der zeile, mindestens drei zeichen, erstes alpha. gefolgt von min 7 zeichen an text oder white space, gefolgt von zufälliger anzahl an text. 
        if re.match(r'^(\w..)[\w\s]{7}(.+)$', inst):
            m=re.match(r'^(\w..)[\w\s]{7}(.+)$', inst)
            mssDict[m.group(1).ljust(9)]=m.group(2)
            # Zergliederung in eine Sigle und eine Text Variable, die auf ein key/value paar aufgeteilt und abgelegt werden.
            msLabelArray.append(m.group(1).ljust(9)) # all mss. label, n: index
            mssDict[msLabelArray[numOfMss]]=re.sub(r'\([^\)]+\)','',mssDict[msLabelArray[numOfMss]]) # remove  ()
            mssDict[msLabelArray[numOfMss]]=re.sub(r'\[[^\]]+\]','',mssDict[msLabelArray[numOfMss]]) # remove  []

            numOfMss+=1 


cut = cut * numOfMss * numOfMss / 2500
# cut: This variable is a threshold for the 'globalLeit' function

    
for msIndex in mssDict.keys():
    msContent = mssDict.get(msIndex)
    msContent = re.sub(r"[\s\|]+", " ", msContent)
    # für jedes label/jeden Text, nimmt den Content und normalisiert wörter
    while re.match(r"^\s*([^\s]+)", msContent): # while another text can be found in $msContent
        m = re.match(r"^\s*([^\s]+)", msContent)
        word = m.group(1)
        msContent = msContent[m.end():]
        # .group(1): the word found
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

    # für jedes Manuskript, geh anhand der Indizes die Label durch und speicher sie weg, außer das erste.

    for otherMsIndex in range(0, msIndex):
        otherMsLabel = msLabelArray[otherMsIndex]
        
        # für jedes Manuskript, geh anhand der Indizes die Label aller anderen Manuscripte durch und speicher sie weg.   

        for word in globalWordCountDict.keys(): # jedes word mit seiner         globalen Anzahl iterieren
            #only words with at least 3 characters are considered
            # wenn die Anzahl der Vorkommnisse des Wortes innerhalb der beiden verglichenen Texte abweicht
            # UND die Anzahl der Vorkommnisse des Wortes innerhalb der beiden verglichenen Texte insgesamt geringer als 2 ist.
                if re.match(r"...", word) and abs(mssWordCountDict[currMsLabel].get(word, 0) - mssWordCountDict[otherMsLabel].get(word, 0)) > 0 and mssWordCountDict[currMsLabel].get(word, 0) + mssWordCountDict[otherMsLabel].get(word, 0) < 2:
                    globalLeit[word] = globalLeit.get(word, 0) + 1

    
    


for word in globalLeit.keys():
    if globalLeit[word] > cut: # Threshhold, ob ein wort dargestellt/verarbeitet werden soll, default = 0, kann noch angepasst werden
        # geht jeden counter für jedes Wort durch und danach in folge jedes andere Wort
        for otherWord in globalLeit.keys():
            # wenn der Counter des Wortes geringer ist, als bei dem verglichenen, dann initiere die variable tab mit 0en (?)
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
                    if debug:
                        vierer(tab[1], tab[2], tab[3], tab, word, otherWord)
                    r = rating(tab[1], tab[2], tab[3], word, otherWord)
                    s = ratings(tab[1], tab[2], tab[3], word, otherWord)
                    if r > 1:
                        ur[word] = ur[word] + (r - 1) ** 2 * s
                        ur[otherWord] = ur[otherWord] + (r - 1) ** 2 * s
                elif tab[1] == 0 and tab[0] > 0 and tab[2] > 0 and tab[3] > 0:
                    if debug:
                        vierer(tab[0], tab[2], tab[3], tab, word, otherWord)
                    r = rating(tab[0], tab[2], tab[3], word, otherWord)
                    s = ratings(tab[0], tab[2], tab[3], word, otherWord)
                    if r > 1:
                        ur[word] = ur[word] + (r - 1) ** 2 * s
                        ur[otherWord] = ur[otherWord] + (r - 1) ** 2 * s
                elif tab[2] == 0 and tab[0] > 0 and tab[1] > 0 and tab[3] > 0:
                    if debug:
                        vierer(tab[0], tab[1], tab[3], tab, word, otherWord)
                    r = rating(tab[0], tab[1], tab[3], word, otherWord)
                    s = ratings(tab[0], tab[1], tab[3], word, otherWord)
                    if r > 1:
                        ur[word] = ur[word] + (r - 1) ** 2 * s
                        ur[otherWord] = ur[otherWord] + (r - 1) ** 2 * s
                elif tab[3] == 0 and tab[0] > 0 and tab[1] > 0 and tab[2] > 0:
                    if debug:
                        vierer(tab[0], tab[1], tab[2], tab, word, otherWord)
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

    # Iterate over all mss and 
    # count the number of mss that contain word
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
    
#Scoremax ist eine Art lowerbound threshold für die Listung von scorewerten        

# Print %ur if debug=1
# logfile
if debug == 1:
    with open("log_py.txt", "w") as log:
        for k in sorted(score, key=lambda x: score[x], reverse=True):
            if ur[k] > 0 and score[k] > scoremax/100:
                log.write(f"{k}  --  {int(score[k])} - {ur[k]} {int(score[k]/scoremax*100)}%\n")
                
# print ins log file pro zeile:
#score (normiert) , ur wert (leitfehlerwert) und den score normiert durch scoremax als prozentsatz der wslkeit.


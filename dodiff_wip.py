#!/usr/bin/python

import re
from collections import defaultdict
import argparse
import csv

  
# defining parameters (user input)
parser = argparse.ArgumentParser(
    prog = 'Leitfehler Detection',
    description= 'A Python Script for detecting Leitfehlers from a given text collation.',
    epilog='Authorship: The original Perl version lf_new4 was written by Dieter Bachmann Philipp, Roelli & Eva Sediki. The lf_new5 was rewritten, optimised and translated into Python by Florian Klement & David Siegl.')

parser.add_argument('-f', '--file', dest='file', required=True, type=str, help='Required: Filepath for the text collation')
parser.add_argument('-c', '--cut', dest='cut', action='store', type=int, default=0, help='Optional: cut off threshold for leitfehler detection')
parser.add_argument('-d', '--debug', dest='debug', action='store', type=int, default=1, choices=[0,1], help='Optional: Binary indicator 0 : only matrix 1 : and a list of pot. leitfehler (lf) and their score')
parser.add_argument('-delim', '--delimiter', dest='delimiter', action='store', type=str, default=',', help='Optional: Delimiter of input file (default: comma)')
parser.add_argument('-e', '--encoding', dest='encoding', action='store', type=str, default='utf-8', help='Optional: Encoding of input file (default: utf-8) See other available options for function open()')
parser.add_argument('-r', '--regex', dest='regex', type=str, default = 0, help='Optional: Filepath to a textfile for additional regex patterns to be substituted within the texts. See the re.sub() format. Example: r"[\s\|]+", ""')

args = parser.parse_args()

cut = args.cut
debug = args.debug
delimiter = args.delimiter
encoding = args.encoding
regex = args.regex


weight = 20 # weight. lf are counted .-times more for the best of them, the others proportionally down to 1

scoremax = 1
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


with open(args.file,'r', newline='', encoding=encoding) as f:
    reader = csv.DictReader(f, delimiter=delimiter)
    for label in reader.fieldnames:
        f.seek(0)
        for inst in reader:
            mssListTemp.append(inst[label])
        mssDictList[label.ljust(9)] = mssListTemp.copy()
        mssListTemp.clear()


msLabelArray = list(mssDictList.keys())
numOfMss = len(msLabelArray)
            
    
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



def diff(list_text1, list_text2):
    temp_diff = []
    for item1, item2 in zip(list_text1, list_text2):
        if item1 != item2:
            if item1 is not None:
                temp_diff.append(item1)
            if item2 is not None:
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
    for sequence in sequenceArray:
        if score.get(word) and scoremax * weight != 0:
            distInHunk += score[word] / scoremax * weight
            distInHunk += 1
    dist += distInHunk
    return int(dist + 0.5)


#dodiff(wordArrayMs1, wordArrayMs2)

print(len(msLabelArray)) # print length of array
print(msLabelArray[0]) # erste zeile
testDict = defaultdict()
testList = []

max_key_length = max([len(key) for key in mssDictList.keys()])

for msIndex in range(1,len(msLabelArray)):
    #print(msLabelArray[msIndex])
    current_key = msLabelArray[msIndex]
    print(current_key, end='')
    # Add spaces to align the labels
    # schreib das label in die zeile
    for otherMsIndex in range(0,msIndex):
        # Anzeil der Zeilen mal Spalten (eg. für den aktuellen Text, geh alle zuvor bearbeiteten durch) und mache pro Element/Text:        
        wordArrayMs1 = mssDictList[msLabelArray[msIndex]]
        wordArrayMs2 = mssDictList[msLabelArray[otherMsIndex]]
        el = dodiff(wordArrayMs1, wordArrayMs2)
    
        print(" {} ".format(el), end='') 
    print()


#Hier wird noch dodiff gecalled, wobei der gesamte content eines textes mit dem gesamten des andereren 
#         ausgegegben und mit whitespaces umrahmt wird.
# jeweils zeilenpaare werden angeschaut und dafür beide Zeilen in Frage ausgegeben:
# A, AB, AC BC, AD BD CD

        # $matrix->assign($msIndex+1,$otherMsIndex+1,$el);
        # $matrix->assign($otherMsIndex+1,$msIndex+1,$el));
        #testList.append(el)
        #testDict[msIndex] = el
   
        #print("")
    

      # assigning a score to the pot. leitfehler in wlist();
            
            
            # calibration to $weight.  
            
######################################################################## --> verschieben, da achronologisch 
            #Interaction von den leitfehler scores, mit den weights
            #weight: lf are counted .-times more for the best of them,
            #the others proportionally down to 1
            #'$weight': This variable is a weight that is applied to the scores 
            #of the differences between lists of words. The script counts the differences 
            #between lists of words multiple times, with the best differences being counted '$weight' 
            #times and the others being counted proportionally down to 1.
            #score =  Wert in der output Pyramide
            
            #Aufrufen der Scorewerte für das Wort, mit der zusätzlichen Gewichtung f
            # für eine größere Anzahl an Abweichungen
            # Was macht scoremax?
            
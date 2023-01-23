#!/usr/bin/python

import os
import re
from collections import defaultdict

scoremax = 1
mssHash={}
msLabelArray=[]
debug = 1
numOfMss=0
score=defaultdict(int)
cut = 0   
cut = cut * numOfMss * numOfMss / 2500
mssWordCountHash = defaultdict(dict)
globalWordCountHash = defaultdict(dict)
leit = []
globalLeit = defaultdict()
ur = defaultdict(int)

def rating(a1, a2, a3, word, otherWord):
    a = [a1, a2, a3]
    r = min(a)

    return r

def ratings(a1, a2, a3, word, otherWord):
    a = [a1, a2, a3]
    s = len(msLabelArray) - max(a) - min(a) # noch nicht sicher, ob so passt (putput Vergleich)

    return s


#Vierer wird in der aktuellen Variante nciht verwendet, da der Fall debug = 3 nicht im Einsatz ist.

def vierer(t0, t1, t2, t3, word, otherWord):
    if debug == 3:
        if t0 != 1 and t1 != 1 and t2 != 1 and t3 != 1:
            print(f"{word}/{otherWord} {t0} {t1} {t2} {t3}")


with open(r'./test_data/besoin-all.txt', 'r') as fp:
    for line in fp:
        inst = line
        inst=inst.strip() # Chop off the last char
        inst=inst.replace(',','').replace('!','').replace('?','').replace('"','') # remove punctuation
        # in=in.replace('.',' ') # remove . ?
        inst=inst.replace(r'\s[^\s]*\*[^\s]*', ' €') # convert word with a *-wildcard to €
        inst=inst.rstrip()
        # label manuscripts (3 chars), or n chars make (n-1) dots in next line
        # Anfang der zeile, mindestens drei zeichen, erstes alpha. gefolgt von min 7 zeichen an text oder white space, gefolgt von zufälliger anzahl an text. 
        if re.match(r'^(\w..)[\w\s]{7}(.+)$', inst):
            m=re.match(r'^(\w..)[\w\s]{7}(.+)$', inst)
            mssHash[m.group(1).ljust(9)]=m.group(2)
            # die nächsten lines sind zu testen, da uns nicht ganz ersichtlich ist, wie sie funktioniert.
            # Vermutung: Zergliederung in eine Siglen und eine Text Variable, die auf ein key/value paar aufgeteilt und abgelegt werden.
            # Variablen + indexierung vermutlich neu zu setzen
            msLabelArray.append(m.group(1).ljust(9))# all mss. label, n: index
            #Reverse engineering bug fixing, überüprufung ob die beiden dicts richtig erstellt wurden und löschen von Klammern
            mssHash[msLabelArray[numOfMss]]=re.sub(r'\([^\)]+\)','',mssHash[msLabelArray[numOfMss]]) # remove  ()
            mssHash[msLabelArray[numOfMss]]=re.sub(r'\[[^\]]+\]','',mssHash[msLabelArray[numOfMss]]) # remove  []

            numOfMss+=1 


   
# cut: This variable is a threshold for the 'globalLeit' function (which is not used in the script). 

# Hash map that contains a hash for each ms; the keys of the inner hash map are words, 
# the value of each word is the number of occurrences of the word in the ms
#{text:{word:count}
# {word:count}}


    
    # Hash map over all words in the mss; the key of the hash map are words, 
    # the value of each word is the number of occurrences of the word over all mss


    

for msIndex in mssHash.keys():
    msContent = mssHash.get(msIndex)
    msContent = re.sub(r"[\s\|]+", " ", msContent)
    #für jedes label/jeden Text, nimm den Content und nomralisiert wörter
    # womöglich wäre die folgende while loop besser als for loop umzusetzen.
    while re.match(r"^\s*([^\s]+)", msContent): # while anohter text can be found in $msContent
        # hier wird der content der variable vermutlich "abegangen" und nach wörtern umrahmt von lehrzeichen gesucht
        # was für das fortfahren im Text deuten würde.
        m = re.match(r"^\s*([^\s]+)", msContent)
        # nimm das erste Element der vorherigen Indexierung von Textelementen über  übersprungene whitespaces
        word = m.group(1)
        msContent = msContent[m.end():]
        # $1: the word found
        # increment counter for the word found in the ms specific word 
        # hash map and in the global word hash map
        
        #for loop iteriert alle texte durch
        #while loop iteriert jedes wort verbunden mit leerzeichen durch
        #wordcount variablen weisen die in der while loop ausgelesenen wörter
        #einem dictionary key zu, der um eins erhöht wird.
        
        '''
        mssWordCountHash = {text:{word:count},
                                {word:count},
                            text:{word:count}
                                {word:count}}
        globalWordCountHash= {{word:count},
                            {word:count},
                            {word:count},
                            {word:count}}
                                                        
        '''
        
        mssWordCountHash[msIndex][word] = mssWordCountHash[msIndex].get(word, 0) + 1
        
        globalWordCountHash[word] = globalWordCountHash.get(word, 0) + 1



    
    # Hash map over all words in the mss; the keys of the hash map are words, 
    # and the value is a counter: how often the word is a leitfehler candidate over all mss

        #the subroutine wlist() calculates a score for each word in the manuscripts based
        # on the number of manuscripts in which it appears and its global frequency
        # in the manuscripts. It also calculates a scoremax value, which is the maximum score 
        # among all the words.


    # finding candidates for leitfehler

        # Matrix of mss that contains a hash map; the keys of the hash map are words
        # and the value is a bool: 1=is a leitfehler candidate, 0=is not a leitfehler candidate


        ################################################################
        ################################################################
        # Die folgenden Codeblöcke sind der Funktion wlist untergeordnet und sind Teil ihrer Prozesse,
        # jedoch verläuft die Zuerdnung und erkennung von Zugehörigkeit noch nicht fehlerfrei.
        # Die Einrückungen und ein mögliches return statement muss noch überdacht werden,
        # spätestens bei folgenden tests mit Mock inhalten.
        
        # '''
        # Wörter die insgesamt weniger als zweimal innerhalb von zwei verglichenen Manuskripten vorkommen und hierbei in beiden nicht gleich oft, 
        # werden als Kandidaten herangezogen.
        # Hierbei werden zwei Counter bespielt, ein globaler und einer für jede spezische Manuskript kombination, 
        # um in einer Abstimmung zur Eingnung von Termen zum Schluss zu dienen.
        # Paare an Leitfehler, die nur in wenigen Texten vorkommen, werden höher bewertet.
        # '''


for msIndex in range(1, len(msLabelArray)):
    currMsLabel = msLabelArray[msIndex]
    
    # für jedes Manuskript, geh anhand der Indizes die Label durch und speicher sie weg, außer das erste.

    for otherMsIndex in range(0, msIndex):
        otherMsLabel = msLabelArray[otherMsIndex]
        # für jedes Manuskript, geh anhand der Indizes die Label aller anderen Manuscripte durch und speicher sie weg.   

        for word in globalWordCountHash.keys(): # jedes word mit seiner         globalen Anzahl iterieren
            #only words with at least 3 characters are considered
            # wenn die Anzahl der Vorkommnisse des Wortes innerhalb der beiden verglichenen Texte abweicht
            # UND die Anzahl der Vorkommnisse des Wortes innerhalb der beiden verglichenen Texte insgesamt geringer als 2 ist.
            #if word in globalLeit:
                if re.match(r"...", word) and abs(mssWordCountHash[currMsLabel].get(word, 0) - mssWordCountHash[otherMsLabel].get(word, 0)) > 0 and mssWordCountHash[currMsLabel].get(word, 0) + mssWordCountHash[otherMsLabel].get(word, 0) < 2:
                    globalLeit[word] = globalLeit.get(word, 0) + 1

                    
                    # setzt counter für wort im localen leitfehler index auf eins (bool, somit setzen, nicht erhöhen)
                    # global wird der vote dafür um eins erhöht.
                    #leit[msIndex][otherMsIndex][word] = 1 
                    # leitfehler-candidate 1 if yes between 2 mss.
                     # leitfehler counter total for each word
                    
                
# 19.11. bis hierhin getestet

################################ debug = entspricht nicht dem default Wert und wird deshalb standardmäßig
### nicht verwendet. In einem späteren Optimierungsschritt ist dieser noch genauer zu betrachten. 


for word in globalLeit.keys():
    if globalLeit[word] > cut: # Threshhold, ob ein wort dargestellt/verarbeitet werden soll, default = 0
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
                    if word in mssWordCountHash[currMsLabel] and otherWord in mssWordCountHash[currMsLabel]:
                        tab[0] += 1
                    #Eine reihe an vergleichen wird aufgestellt:
                    #Wort1 und Wort2 weeden daraufhin verglichen, ob eines der beiden, beide oder keines in einem manuskript 
                    #enthalten ist oder nicht
                    # Only word is in the the current ms
                    elif word in mssWordCountHash[currMsLabel] and otherWord not in mssWordCountHash[currMsLabel]:
                        tab[1] += 1
                    # Only otherWord is in the the current ms
                    elif word not in mssWordCountHash[currMsLabel] and otherWord in mssWordCountHash[currMsLabel]:
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

        if mssWordCountHash[currMsLabel].get(word, 0) != 0:
            counter += 1
    
    # Geh jedes Wort durch, geh jeden Text durch, speicher beides in in eine temp variable, 
    # wenn das wort mindestens einmal vorkommt, erhöh ihren Counter um eins.  
    
    if counter > numOfMss/2:
        counter = numOfMss - counter
    
    #Wenn das Wort häufiger als in jedem zweiten Text vorkommt, 
    #dann reduzier den Wert um die Anzahl der texte.
    
    #ur, which stores the scores for each leitfehler candidate,
    #the scores in ur are then normalized by dividing them by the number of occurrences of
    #each leitfehler candidate in the manuscripts, and the resulting values are stored in a 
    #hash map called %score (?)

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
if debug > 0:
    with open("log_py.txt", "w") as log:
        for k in sorted(score, key=lambda x: score[x], reverse=True):
            if ur[k] > 0 and score[k] > scoremax/100:
                log.write(f"{k}  --  {int(score[k])} - {ur[k]} {int(score[k]/scoremax*100)}%\n")
                    
    # print ins log file pro zeile: (?)
    #score (normiert) , ur wert (leitfehlerwert) und den score normiert durch scoremax als prozentsatz der wslkeit.  (?)



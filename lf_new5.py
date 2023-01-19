#!/usr/bin/python

import sys
#import difflib
import re
import string # noch checken
from collections import defaultdict


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
        if re.match(r'^(\w..)[\w\s]{7}(.+)$', inst):
            m=re.match(r'^(\w..)[\w\s]{7}(.+)$', inst)
            mssHash[m.group(1).ljust(9)]=m.group(2)
            # die nächsten lines sind zu testen, da uns nicht ganz ersichtlich ist, wie sie funktioniert.
            # Vermutung: Zergliederung in eine Siglen und eine Text Variable, die auf ein key/value paar aufgeteilt und abgelegt werden.
            # Variablen + indexierung vermutlich neu zu setzen
            msLabelArray.append(m.group(1).ljust(9))# all mss. label, n: index
            print(msLabelArray)
            #Reverse engineering bug fixing, überüprufung ob die beiden dicts richtig erstellt wurden und löschen von Klammern
            mssHash[msLabelArray[numOfMss]]=re.sub(r'\([^\)]+\)','',mssHash[msLabelArray[numOfMss]]) # remove  ()
            mssHash[msLabelArray[numOfMss]]=re.sub(r'\[[^\]]+\]','',mssHash[msLabelArray[numOfMss]]) # remove  []

            numOfMss+=1

#wlist()  # call einer weiter unten definierten Funktion
# remove to get a fast result without calculating the lff

######################################################################## --> verschieben, da achronologisch 
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

######################################################################## --> verschieben, da achronologisch 
#trickle down economics, die unsichtbare hand des marktes regelt
#jeweils zeilenpaare werden angeschaut und dafür beide Zeilen in Frage ausgegeben:
#A, AB, AC BC, AD BD CD

        #Hier wird noch dodiff gecalled, wobei der gesamte content eines textes mit dem gesamten des andereren 
        # ausgegegben und mit whitespaces umrahmt wird.
        # (diff
        #my $el=dodiff(\@wordArrayMs1, \@wordArrayMs2);
        #print " ".$el." ";
        #$matrix->assign($msIndex+1,$otherMsIndex+1,$el); 
        #$matrix->assign($otherMsIndex+1,$msIndex+1,$el)); 


def dodiff(a1, a2):
    wordArrMs1 = a1
    wordArrMs2 = a2

# Copy the two arrays passed to this subroutine into 
# the variables wordArrMs1 and wordArrMs2

    # diff computes the smallest set of additions and deletions necessary to turn the first sequence into the second
    # and returns a 2-dim array of differences (hunks with sequences); 
    # each difference is a list of 3 elements (-/+, position of the change, string), e.g.:
    # [ 
    #   [ 
    #      [ '-', 0, 'a' ] 
    #   ],
    #   [ 
    #      [ '-', 8, 'n' ], 
    #      [ '+', 9, 'p' ]
    #   ]
    # ]
# Sind die Abänderungen innerhalb des Beispieloutputs in eine oder in beide Richtungen?
# Sind die einzelnen Arrays für jede Zeile zu verstehen? Chaacter Sequences oder einzelne Zeichen?

    diffArray = diff(wordArrMs1, wordArrMs2)

    dist = 0
    for hunk in diffArray:
        sequenceArray = hunk
        distInHunk = 0
        for sequence in sequenceArray:
      # assigning a score to the pot. leitfehler in wlist();
            word = " ".join(sequence) # Concatenate 3 elements of the list
             # Remove +/- at the beginning and the digits (\d) of the position;
             # leave only the char string
            word = re.sub(r"^. \d+ (.+)", r"\1", word) # $1 contains the first match: (.+)
            # substitute the entire output of one line of diff with the character at the end of it and save into word
            #handpicked lf
            #if($word=~/(definitio|tumore|cognoscere|proiciunt|afixia|introrsum|irruit|uisceribus|retentione|aperiant|molitam|catarticum|efficitur|sursum)/){$distInHunk+=$weight} # handpicked lf

        # Als möglichen Parameter implementieren, ob wildcards aus der Gewichtung ausgenommen werden sollen
        # Generelle Filterfunktionsmöglichkeiten?
            #if($word=~/€/){$distInHunk=-2} # €-wildcard matches anything
            
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
            
            if score.get(word) and scoremax * weight != 0:
                distInHunk += score[word] / scoremax * weight
            distInHunk += 1
        dist += distInHunk
     
     # Die Zähler für die Anzahl der insgesamten Abweichungen pro Text und die für
     # die Anzahl der Seuqenzen werden vereint.
        
   #$dist=$#diffArray+1;
    return int(dist + 0.5)

# Natürliches, kaufmännsiches Runden wird simuliert.

##################################
##################################

# Content vom Block vor dodiff, nach der Normaliserung, zum Erstellen der Püramide und Befüllen.
# Hier mit dem fehlenden Block, der den Inhalt processiert und die Funktion called. In welcher Reiehenfolge
# die Funktionen angeordnet wqrden sollen, wird sich noch im Testen mit wirklichem Inhalt ergeben müssen.


#msLabelArray = []  # vermutlich nicht gebraucht, und überschreibt nur Input
#mssHash = {}       # vermutlich nicht gebraucht, und überschreibt nur Input

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
    
#####################################


def wlist():
    global cut
    cut = cut * numOfMss * numOfMss / 2500
    
# cut: This variable is a threshold for the 'globalLeit' function (which is not used in the script). 

# Hash map that contains a hash for each ms; the keys of the inner hash map are words, 
# the value of each word is the number of occurrences of the word in the ms
#{text:{word:count}
# {word:count}}

mssWordCountHash = defaultdict(dict)
    
    # Hash map over all words in the mss; the key of the hash map are words, 
    # the value of each word is the number of occurrences of the word over all mss

globalWordCountHash = {}
    
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

    '''
        Wörter die insgesamt weniger als zweimal innerhalb von zwei verglichenen Manuskripten vorkommen und hierbei in beiden nicht gleich oft, 
        werden als Kandidaten herangezogen.
        Hierbei werden zwei Counter bespielt, ein globaler und einer für jede spezische Manuskript kombination, 
        um in einer Abstimmung zur Eingnung von Termen zum Schluss zu dienen.
        Paare an Leitfehler, die nur in wenigen Texten vorkommen, werden höher bewertet.
        '''


    for msIndex in range(1, len(msLabelArray)):
        currMsLabel = msLabelArray[msIndex]
        
    # für jedes Manuskript, geh anhand der Indizes die Label durch und speicher sie weg, außer das erste.

        for otherMsIndex in range(0, msIndex):
            otherMsLabel = msLabelArray[otherMsIndex]
            
        # für jedes Manuskript, geh anhand der Indizes die Label aller anderen Manuscripte durch und speicher sie weg.   

            for word in globalWordCountHash.keys(): # jedes word mit seiner globalen Anzahl iterieren
                #only words with at least 3 characters are considered
                # wenn die Anzahl der Vorkommnisse des Wortes innerhalb der beiden verglichenen Texte abweicht
                # UND die Anzahl der Vorkommnisse des Wortes innerhalb der beiden verglichenen Texte insgesamt geringer als 2 ist.
                if re.match(r"...", word) and abs(mssWordCountHash[currMsLabel][word] - mssWordCountHash[otherMsLabel][word]) > 0 \
                    and mssWordCountHash[currMsLabel][word] + mssWordCountHash[otherMsLabel][word] < 2:
                        # setzt counter für wort im localen leitfehler index auf eins (bool, somit setzen, nciht erhöhen)
                        # global wird der vote dafür um eins erhöht.
                    leit[msIndex][otherMsIndex][word] = 1 # leitfehler-candidate 1 if yes between 2 mss.
                    globalLeit[word] = globalLeit.get(word, 0) + 1 # leitfehler counter total for each word
                    
                    #print "$currMsLabel $otherMsLabel: $word ".$mssWordCountHash{$currMsLabel}{$word}."/".$mssWordCountHash{$otherMsLabel}{$word}."\n"
    
    ################################ debug = entspricht nicht dem default Wert und wird deshalb standardmäßig
    ### nicht verwendet. In einem späteren Optimierungsschritt ist dieser noch genauer zu betrachten. 
    
    '''
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
                        '''
    ur = {}

    for word in globalLeit.keys():
        if globalLeit[word] > cut: # Threshhold, ob ein wort dargestellt/verarbeitet werden soll, defunct (0)
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

#################################################################################################
#################################################################################################
# im Perl Skript ist für den folgenden Block, für je einen Fall, jeweil eine eigenen Variante gelistet.
# die drei fehlenden müssen noch kreeiert werden.


                    # Both words occur together in no ms
                    if tab[0] == 0 and tab[1] > 0 and tab[2] > 0 and tab[3] > 0:
                    # Sie schließen sich gegenseitig aus - kommen nciht gemeinsam, aber getrennt in unterschiedlichen Texten vor
                    # nur wenn der erste 0 ist, kommen die anderen Funktionen zum Einsatz, die auf die weiteren drei Spalten wirken.
                    # nochmal zu überprüfen (?)  
                        if debug:
                            vierer(tab[1], tab[2], tab[3], tab, word, otherWord)
                        r = rating(tab[1], tab[2], tab[3], word, otherWord)
                        s = ratings(tab[1], tab[2], tab[3], word, otherWord)
                        if r > 1:
                            ur[word] = ur.get(word, 0) + (r - 1)**2*s
                            ur[otherWord] = ur.get(otherWord,0) + (r - 1)**2*s
                            
                            
#################################################################################################
#################################################################################################

#Counter/Nr. of occurences ist unabhängig von der Matrix zuvor, das relationale Auftreten von einem Wort
# im Verhältnis zu anderen steht nicht mit dem absoluten im Konflikt.

    # Calculate counter: number of occurences of word 
    for word in globalLeit:
        counter = 0

        # Iterate over all mss and 
        # count the number of mss that contain word
        for msIndex in range(1, len(msLabelArray)):
            currMsLabel = msLabelArray[msIndex]

            if mssWordCountHash[currMsLabel][word] != 0:
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
        with open("log", "w") as log:
            for k in sorted(score, key=score.get, reverse=True):
                if ur[k] > 0 and score[k] > scoremax/100:
                    log.write(f"{k}  --  {int(score[k])} - {ur[k]} {int(score[k]/scoremax*100)}%\n")
                    
    # print ins log file pro zeile: (?)
    #score (normiert) , ur wert (leitfehlerwert) und den score normiert durch scoremax als prozentsatz der wslkeit.  (?)

def rating(a1, a2, a3, word, otherWord):
    a = [a1, a2, a3]
    r = min(a)

    return r

def ratings(a1, a2, a3, word, otherWord):
    a = [a1, a2, a3]
    s = len(msLabelArray) - (max(a)) - (min(a))

    return s


#Vierer wird in der aktuellen Variante nciht verwendet, da der Fall debug = 3 nicht im Einsatz ist.

def vierer(a1, a2, a3, t0, t1, t2, t3, word, otherWord):
    if debug == 3:
        if t0 != 1 and t1 != 1 and t2 != 1 and t3 != 1:
            print(f"{word}/{otherWord} {t0} {t1} {t2} {t3}")
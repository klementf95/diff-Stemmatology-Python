#!/usr/bin/python

import os
import re

mssHash={}
msLabelArray=[]

# standardisation
numOfMss=0

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
            print(msLabelArray)
            #Reverse engineering bug fixing, überüprufung ob die beiden dicts richtig erstellt wurden und löschen von Klammern
            mssHash[msLabelArray[numOfMss]]=re.sub(r'\([^\)]+\)','',mssHash[msLabelArray[numOfMss]]) # remove  ()
            mssHash[msLabelArray[numOfMss]]=re.sub(r'\[[^\]]+\]','',mssHash[msLabelArray[numOfMss]]) # remove  []

            numOfMss+=1  


print(len(msLabelArray)) # print length of array
print(msLabelArray[0]+'\n') # erste zeile

for msIndex in range(1,len(msLabelArray)):
    print(msLabelArray[msIndex])
    # schreib das label in die zeile
    for otherMsIndex in range(0,msIndex):
        # Anzeil der Zeilen mal Spalten (eg. für den aktuellen Text, geh alle zuvor bearbeiteten durch) und mache pro Element/Text:
        wordArrayMs1 = mssHash[msLabelArray[msIndex]].split(' ') 
# split content of this ms into words
        wordArrayMs2 = mssHash[msLabelArray[otherMsIndex]].split(' ')




def wlist():
    global cut
    cut = cut * numOfMss * numOfMss / 2500
    
# cut: This variable is a threshold for the 'globalLeit' function (which is not used in the script). 

# Hash map that contains a hash for each ms; the keys of the inner hash map are words, 
# the value of each word is the number of occurrences of the word in the ms
#{text:{word:count}
# {word:count}}

    mssWordCountHash = {}
    
    # Hash map over all words in the mss; the key of the hash map are words, 
    # the value of each word is the number of occurrences of the word over all mss
     
    globalWordCountHash = {}

    for msIndex in mssHash.keys():
        msContent = mssHash[msIndex]
        msContent = re.sub(r"[\s\|]+", " ", msContent)
        #für jedes label/jeden Text, nimm den Content und lösch Zeilenumbrüche raus
        # womöglich wäre die folgende while loop besser als for loop umzusetzen.
        while re.match(r"^\s*([^\s]+)", msContent): # while a word can be found in $msContent
            # heir wird der content der variable vermutlich "abegangen" und nach wörtern umrahmt von lehrzeichen gesucht
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

    leit = []
    globalLeit = {}
    
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
    
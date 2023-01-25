from collections import defaultdict
import re
import csv

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

mssDictList = defaultdict(list)
mssListTemp = []


with open(r'./test_data/besoin_test.csv','r', newline='', encoding='utf-8') as fp:
    reader = csv.DictReader(fp, delimiter=',')
    for label in reader.fieldnames:
        fp.seek(0)
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
    ms = [word.replace(',','').replace('!','').replace('?','').replace('"','').replace('.','').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(r'\s[^\s]*\*[^\s]*', ' €') for word in ms]
    mssDictList[key] = ms



print(mssDictList['A        '])
        

print(len(msLabelArray)) # print length of array
print(msLabelArray[0]) # erste zeile

for msIndex in range(1,len(msLabelArray)):
    print(msLabelArray[msIndex])
    # schreib das label in die zeile
    for otherMsIndex in range(0,msIndex):
        # Anzeil der Zeilen mal Spalten (eg. für den aktuellen Text, geh alle zuvor bearbeiteten durch) und mache pro Element/Text:
        wordArrayMs1 = mssDict[msLabelArray[msIndex]].split(' ') # split content of this ms into words
        wordArrayMs2 = mssDict[msLabelArray[otherMsIndex]].split(' ')# split content of the other ms into words

####################################################################### --> verschieben, da achronologisch 
# trickle down economics, die unsichtbare hand des marktes regelt
# jeweils zeilenpaare werden angeschaut und dafür beide Zeilen in Frage ausgegeben:
# A, AB, AC BC, AD BD CD

#         Hier wird noch dodiff gecalled, wobei der gesamte content eines textes mit dem gesamten des andereren 
#         ausgegegben und mit whitespaces umrahmt wird.
        (diff
        my $el=dodiff(\@wordArrayMs1, \@wordArrayMs2);
        print " ".$el." ";
        $matrix->assign($msIndex+1,$otherMsIndex+1,$el); 
        $matrix->assign($otherMsIndex+1,$msIndex+1,$el)); 



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
# Natürliches, kaufmännisches Runden wird simuliert.

##################################
##################################

# Content vom Block vor dodiff, nach der Normaliserung, zum Erstellen der Püramide und Befüllen.
# Hier mit dem fehlenden Block, der den Inhalt processiert und die Funktion called. In welcher Reiehenfolge
# die Funktionen angeordnet wqrden sollen, wird sich noch im Testen mit wirklichem Inhalt ergeben müssen.


#msLabelArray = []  # vermutlich nicht gebraucht, und überschreibt nur Input
#mssDict = {}       # vermutlich nicht gebraucht, und überschreibt nur Input

print(len(msLabelArray))
print(msLabelArray[0])

for msIndex in range(1, len(msLabelArray)):
    print(msLabelArray[msIndex])
    for otherMsIndex in range(0, msIndex):
        wordArrayMs1 = mssDict[msLabelArray[msIndex]].split(" ")
        wordArrayMs2 = mssDict[msLabelArray[otherMsIndex]].split(" ")

        el = dodiff(wordArrayMs1, wordArrayMs2)
        print(" {} ".format(el))
    print("")
    
#####################################
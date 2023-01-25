from collections import defaultdict
import re
import csv

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


with open('./test_data/besoin_test.csv','r', newline='', encoding='utf-8') as fp:
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
    ms = [word.replace(',','').replace('!','').replace('?','').replace('"','').replace('.','').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(r'\s[^\s]*\*[^\s]*', ' €').replace('\r\n', '') for word in ms]
    mssDictList[key] = ms
    mssDict[key] = "".join(mssDictList[key])
    ms = [word.replace(' ','') for word in ms]
    mssDictList[key] = ms


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
        print(hunk)
        #for sequence in sequenceArray:
            #print(sequence)

#dodiff(wordArrayMs1, wordArrayMs2)



#print(len(msLabelArray)) # print length of array
#print(msLabelArray[0]) # erste zeile


for msIndex in range(1,len(msLabelArray)):
    print(msLabelArray[msIndex])
    # schreib das label in die zeile
    for otherMsIndex in range(0,msIndex):
        # Anzeil der Zeilen mal Spalten (eg. für den aktuellen Text, geh alle zuvor bearbeiteten durch) und mache pro Element/Text:        
        wordArrayMs1 = mssDictList[msLabelArray[msIndex]]
        wordArrayMs2 = mssDictList[msLabelArray[otherMsIndex]]
        el = dodiff(wordArrayMs1, wordArrayMs2)
        print(el)
        #print(" {} ".format(el))
        #print("")


      # assigning a score to the pot. leitfehler in wlist();
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
            
        #     if score.get(word) and scoremax * weight != 0:
        #         distInHunk += score[word] / scoremax * weight
        #     distInHunk += 1
        # dist += distInHunk
     
     # Die Zähler für die Anzahl der insgesamten Abweichungen pro Text und die für
     # die Anzahl der Seuqenzen werden vereint.
        
   #$dist=$#diffArray+1;
    #return int(dist + 0.5)
# Natürliches, kaufmännisches Runden wird simuliert.

# jeweils zeilenpaare werden angeschaut und dafür beide Zeilen in Frage ausgegeben:
# A, AB, AC BC, AD BD CD

#         Hier wird noch dodiff gecalled, wobei der gesamte content eines textes mit dem gesamten des andereren 
#         ausgegegben und mit whitespaces umrahmt wird.
        # (diff
        # my $el=dodiff(\@wordArrayMs1, \@wordArrayMs2);
        # print " ".$el." ";
        # $matrix->assign($msIndex+1,$otherMsIndex+1,$el); 
        # $matrix->assign($otherMsIndex+1,$msIndex+1,$el)); 

    #     el = dodiff(wordArrayMs1, wordArrayMs2)
    #     print(" {} ".format(el))
    # print("")
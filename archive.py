# standardisation        
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
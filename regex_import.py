from collections import defaultdict
import re
import csv
import argparse

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
weight = 20

mssDictList = defaultdict(list)
mssListTemp = []

# parser = argparse.ArgumentParser(
#     prog = 'Leitfehler Detection',
#     description= 'A Python Script for detecting Leitfehlers from a given text collation.',
#     epilog='Authorship: The original Perl version lf_new4 was written by Dieter Bachmann Philipp, Roelli & Eva Sediki. The lf_new5 was rewritten, optimised and translated into Python by Florian Klement & David Siegl.')

# parser.add_argument('-r', '--regex', dest='regex',  required=False, help=""Filepath to a textfile for additional regex patterns to be substituted within the texts.(optional)
#  See the re.sub format. Example: r'[\s\|]+', '' ' "")
# args = parser.parse_args()


with open('./test_data/coco-besoin.csv','r', newline='', encoding='utf-8') as fp:
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
    with open("./test_data/one_regex_to_rule_them_all.txt") as f:
        for inst in f:
            ms = [re.sub(inst, word) for word in ms]
            print(ms)
            mssDictList[key] = ms


    mssDict[key] = "".join(mssDictList[key])
    ms = [word.replace(' ','') for word in ms]
    mssDictList[key] = ms


#print(mssDictList)

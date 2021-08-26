# -*- coding: utf-8 -*-
"""
Stefan / Kairntech, Sept 2020 modified by Bruno 13 March 2021

This script allows to to compare/evaluate a dataset(json) exported from sherpa that contains the manual 
annotations with a second json that results from sending via the API the same corpus to Sherpa to get 
the automatic annotations (created with anotatesherpadataset.py)

You then call this script with the two json files and a file name where the result (TAB separated table)
will be writte to. 

You will get the list of entities and the respective numbers for recall, precision and how many times
the entity has been found correctly, how many false positives and negatives and examples for these cases. 

Attention / TODO: 
- the script requires identical spans! partial extraction will count as an error    
- there may be counting errors when an entity is found several times in a segment
- recall an Precision for the Types and overall not written into the Excel list, only to STDOUT
- I send the complete corpus, but document have been used to train the model in Sherpa... so the
  results will by systematically too high.

Still: the resulting Excel table allows (after "format as table") to quickly focus on entities
that are often not found or that are often not found, etc ...      
"""

import sys
import json
import argparse
from   collections import defaultdict

manualdocs    = defaultdict(dict)
automaticdocs = defaultdict(dict)

with open(sys.argv[1], encoding="utf-8") as json_file:
    _manualdocs = json.load(json_file)
    for doc in _manualdocs:
        ident = doc['identifier']
        manualdocs[ident] = doc
        
with open(sys.argv[2], encoding="utf-8") as json_file:
    _automaticdocs = json.load(json_file)
    for doc in _automaticdocs:
        ident = doc['identifier']
        automaticdocs[ident] = doc
            
# sanity check
num_manual = 0
for ident in manualdocs:
    num_manual += 1
    if ident not in automaticdocs:
        print("document %s not found in automatic corpus" % ident)
num_automatic = 0
for ident in automaticdocs:
    num_automatic += 1
    if ident not in manualdocs:
        print("document %s not found in manual corpus" % ident)
print("we have %s documents in the manual corpus and %s in the automatic corpus" % (num_manual, num_automatic))

# Bookkeeping
Correct       = 0
FalseNegative = 0
FalsePositive = 0
CorrectEntity       = defaultdict(int)
FalseNegativeEntity = defaultdict(int)
FalsePositiveEntity = defaultdict(int) 
CorrectType         = defaultdict(int)
FalseNegativeType   = defaultdict(int)
FalsePositiveType   = defaultdict(int) 
All = 0 
AllEntity           = defaultdict(int)
AllType             = defaultdict(int)

FalseNegativeSegment= defaultdict(dict)
FalsePositiveSegment= defaultdict(dict)

# now first search for missed entities
for ident in manualdocs:
    
        docname = manualdocs[ident]['identifier']
        segtext = manualdocs[ident]['text'].replace('\n', ' ').replace("\t", " ").replace("\r", "")
        
        manualdoc = manualdocs[ident]
        manualannotations = manualdoc['annotations']
        
        automaticdoc = automaticdocs[ident]
        automaticannotations = automaticdoc['annotations']
        
        manualentities    = [(anno['text'].replace('\n', '').replace("\t", "").replace("\r", ""),anno['labelName']) for anno in manualannotations]
        automaticentities = [(anno['text'].replace('\n', '').replace("\t", "").replace("\r", ""),anno['labelName']) for anno in automaticannotations]

        print("")
        print(ident)
        print("")
        
        print("manual")

        manualentities_without_duplicates = []
        for i in manualentities:
            #annotated non-recoverable costs ("frais irrepetibles") are by design non-redundant. Other labels may have duplicate (redundant) annotations. Quality must be computed on strictly useful annotations.
            if i not in manualentities_without_duplicates or i[1] == 'frais_irrepetibles':
                manualentities_without_duplicates.append(i)
                print(i)
        print("auto")
        
        automaticentities_without_duplicates = []
        for i in automaticentities:        
            if i not in automaticentities_without_duplicates or i[1] == 'frais_irrepetibles':
                automaticentities_without_duplicates.append(i)
                print(i)
        
        for me in manualentities_without_duplicates:
            meE = me[0]
            meT = me[1]
            All += 1
            AllEntity[meE] += 1
            AllType[meT] += 1
            if me not in automaticentities_without_duplicates:
                FalseNegative += 1
                FalseNegativeEntity[meE] += 1
                FalseNegativeType[meT] += 1     
                FalseNegativeSegment[meE][segtext] = 1
                #print("Entity %s labelled %s is missing in doc %s" % (meE.encode('ascii','ignore'), meT.encode('ascii','ignore'), docname.encode('ascii','ignore')))
            else:
                Correct += 1
                CorrectEntity[meE] += 1
                CorrectType[meT] += 1
                #print("Entity %s was found in doc %s" % (meE.encode('ascii','ignore'), docname.encode('ascii','ignore')))
                
        for ae in automaticentities_without_duplicates:
            aeE = ae[0]
            aeT = ae[1]
            if ae not in manualentities_without_duplicates:
                FalsePositive += 1
                FalsePositiveEntity[aeE] += 1
                FalsePositiveType[aeT] += 1
                FalsePositiveSegment[aeE][segtext] = 1
                #print("Entity %s labelled %s wrongly found in doc %s" % (aeE.encode('ascii','ignore'), aeT.encode('ascii','ignore'), docname.encode('ascii','ignore')))

print("")
Recall = Correct / (Correct + FalseNegative)
Precision = Correct / (Correct + FalsePositive)

print("Recall = %.2f" % Recall)
print("Precision = %.2f" % Precision)

for t in AllType: 
    r = 0
    p = 0
    c = CorrectType[t]
    m = FalseNegativeType[t]
    f = FalsePositiveType[t]
    if c+m > 0:
        r = c/(c+m)
    if c+f > 0:
        p = c/(c+f)
    print("Type: %s, recall = %.2f, precision = %.2f" % (t, r, p))

# -*- coding: utf-8 -*-
"""
Bruno Mathis, 18/08/2021

"""

import sys
import json
from collections import defaultdict
from datetime import datetime
filename = sys.argv[1] 

class Decision:
    def __init__(self, identifier, title, metadata, text, sentences):
        self.identifier = identifier
        self.title = title
        self.metadata = metadata
        self.text = text
        self.sentences = sentences
        self.annotations = []
        
class Annotation:
    def __init__(self, text, labelName, start, end, createdBy, createdDate, modifiedDate, status, label):
        self.text = text
        self.labelName = labelName
        self.start = start
        self.end = end
        self.createdBy = createdBy
        self.createdDate = createdDate
        self.modifiedDate = modifiedDate
        self.status = status
        self.label = label       
        
def serializing(obj):
    if isinstance(obj, Decision):
        return {
            "identifier":obj.identifier,
            "title":obj.title,
            "metadata":obj.metadata,
            "text":obj.text,
            "sentences": obj.sentences,
            "annotations": obj.annotations}
            
    if isinstance(obj, Annotation):
        return {
            "text":obj.text,
            "labelName":obj.labelName,
            "start":obj.start,
            "end":obj.end,
            "createdBy":obj.createdBy,
            "createdDate":obj.createdDate,
            "modifiedDate":obj.modifiedDate,
            "status":obj.status,
            "label":obj.label}
    raise TypeError(repr(obj) + " n'est pas sérialisable !")

nb_newanno = 0
with open(filename,encoding="utf-8") as json_file:
    manualdocs = json.load(json_file)
    decisions = []
    old = defaultdict(int)
    new = defaultdict(int)
    nb_oldanno = 0
    for doc in manualdocs:
        starts = []
        decision = Decision(doc['identifier'],doc['title'],doc['metadata'],doc['text'], doc['sentences'])
        length = len(doc['text'])
        for anno in doc['annotations']:
            if anno['status'] ==  "OK":
                nb_oldanno +=1
                annotation = Annotation(anno['text'],anno['labelName'],anno['start'],anno['end'],anno['createdBy'],anno['createdDate'],anno['modifiedDate'],anno['status'],anno['label'])
                decision.annotations.append(annotation)
                starts.append(anno['start'])
                old[anno['labelName']] += 1

        for anno in doc['annotations']:
            if anno['status'] ==  "OK":
            #non recoverable costs should not be propagated, because they will be summed up together after training.
            #Requested costs should not be confused with granted costs. This is the only label which depends on its relative place within the decision
                if anno['labelName'] != "frais_irrepetibles":
                    indx = 0
                    while indx < length:
                        indx = doc['text'].find(anno['text'], indx)
                        if indx == -1:
                            indx = length
                        else:
                            if indx not in starts:
                                annotation = Annotation(anno['text'],anno['labelName'],indx,indx+len(anno['text']),"extend",str(datetime.now()),str(datetime.now()),"OK",anno['label'])
                                decision.annotations.append(annotation)
                                starts.append(indx)
                                nb_newanno +=1
                                print(doc['identifier']+";"+anno['text']+";"+anno['labelName']+";"+str(indx))
                                new[anno['labelName']] += 1
                            indx += len(anno['text'])+1
        decisions.append(decision)
print("")
print("Number of manually-entered annotations : %s" % nb_oldanno)
print("Number of automatically replicated annotations : %s" % nb_newanno)
print("")
print("Breakdown of automatically replicated annotations")
for t in old:
    rate = new[t]/old[t]
    print("%s, existing annotations %s, replicated annotations %s, rate %.2f" % (t, old[t], new[t], rate))
print("")
with open("propagated_"+filename, 'w', encoding='utf-8') as f:
    json.dump(decisions, f, default=serializing, indent=4,ensure_ascii=False)
# -*- coding: utf-8 -*-
"""
Bruno Mathis, 18/07/2021
This program reduces a fully annotated corpus to a smaller file limited to legal citations annotations
It is also possible to restrict the outgoing file to a range of decisions
The resulting file will be easier to upload to a project where other labels will not be used.

"""

import sys
import json
from collections import defaultdict
from datetime import datetime
filename = sys.argv[1] 
start = int(sys.argv[2])
end = int(sys.argv[3])

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

with open(filename,encoding="utf-8") as json_file:
    manualdocs = json.load(json_file)
    decisions = []
    num_dec = 0
    num_anno = 0
    i = 0
    for doc in manualdocs:
        i += 1
        if i >= start and i <= end:
            decision = Decision(doc['identifier'],doc['title'],doc['metadata'],doc['text'], doc['sentences'])
            for anno in doc['annotations']:
                if anno['label'] == "Reference Juridique" and anno['status'] ==  "OK":
                    annotation = Annotation(anno['text'],anno['labelName'],anno['start'],anno['end'],anno['createdBy'],anno['createdDate'],anno['modifiedDate'],anno['status'],anno['label'])
                    decision.annotations.append(annotation)
                    num_anno += 1
            decisions.append(decision)
            num_dec += 1      
print("Number of extracted decisions = %s" % num_dec)
print("Number of extracted annotations = %s" % num_anno)
   
with open("reduced_"+filename, 'w', encoding='utf-8') as f:
    json.dump(decisions, f, default=serializing, indent=4,ensure_ascii=False)

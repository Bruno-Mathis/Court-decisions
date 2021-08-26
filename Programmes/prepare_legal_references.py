# -*- coding: utf-8 -*-
"""
Bruno Mathis, 18/08/2021
This program builds an adhoc corpus where every document is made of the list of manually-entered and propagated legal citations for each court decision.

"""
import json
import datetime
import sys
filename = sys.argv[1]    
decisions = []
nb_dec = 0

class Decision:
    def __init__(self, identifier, legal_citations, nb_legal_citations, multiple_reference_citations):
        self.identifier = identifier
        self.legal_citations = legal_citations
        self.nb_legal_citations = nb_legal_citations
        self.multiple_reference_citations = multiple_reference_citations

def serializing(obj):
    if isinstance(obj, Decision):
        return {
            "identifier": obj.identifier,
            "text":obj.legal_citations,
            "nb legal citations":obj.nb_legal_citations}
    raise TypeError(repr(obj) + " n'est pas sérialisable !")

with open(filename,encoding="utf-8") as json_file:
    docs = json.load(json_file)
    for i in docs:
        #decisions metadata show up in the very first annotations
        identifier = i['identifier']
        legal_citations = []
        nb_legal_citations = 0
        multiple_reference_citations = 0
        for j in i['annotations']:
            if j['labelName']=="reference_juridique":
                nb_legal_citations +=1
                legal_citation= j['text'].replace("et suivants ","").replace("à ","et ").replace("/n","")
                legal_citations.append(legal_citation)
                #one single annotation may involve several articles from several codes or laws
                position = 0
                multiple_reference = False
                #for each comma in the citation, the citation is duplicated
                while position > -1:
                    position = legal_citation.find(",", position)
                    #print(i['identifier']+" ; "+legal_citation+str(legal_citation.find(" et ", position))+" ; "+str(legal_citation.find(",", position))+" ; "+str(position))
                    if position > -1:
                        multiple_reference = True
                        legal_citations.append(legal_citation)
                        position +=1
                position = 0
                #for each operand "et" in the citation, the citation is duplicated
                while position > -1:
                    position = legal_citation.find("et ", position)
                    if position > -1:
                        multiple_reference = True
                        legal_citations.append(legal_citation)
                        position +=1
                if multiple_reference is True:
                    multiple_reference_citations += 1
        #the decision is appended to other decisions already recorded
        legal_citations = "\n".join(legal_citations)
        if nb_legal_citations > 0:
            nb_dec+=1
            decisions.append(Decision(i['identifier'], legal_citations, nb_legal_citations, multiple_reference_citations))
            print(i['identifier']+" ; "+str(nb_dec)+" ; "+str(nb_legal_citations)+" ; "+str(multiple_reference_citations))
                     
with open('citations_list_'+filename, 'w', encoding='utf-8') as f:
    json.dump(decisions, f, default=serializing, indent=4,ensure_ascii=False)

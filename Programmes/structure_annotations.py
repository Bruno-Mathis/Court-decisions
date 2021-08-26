import json
import datetime
import sys
filename = sys.argv[1]    
decisions = []
nb_dec = 0

class Decision:
    def __init__(self, identifier, nb_annotations, jurisdiction, decision_chamber, date, appeal_number, ecli, referral_court):
        self.identifier = identifier
        self.nb_annotations = nb_annotations
        self.jurisdiction = jurisdiction
        self.decision_chamber = decision_chamber
        self.date = date
        self.cassation_id = cassation_id
        self.ecli = ecli
        self.referral_court = referral_court
        self.appellants = []
        self.defendants = []
        self.legal_references = []
        self.case_law_references = []
        self.proceedings = []
        self.cassation_appeals = []
        self.appeals = []
        self.solutions = []
        self.unrecoverable_costs = []
        
class Proceeding:
    def __init__(self, start, date, event_type, jurisdiction, chamber):
        self.start = start
        self.date = date
        self.event_type = event_type
        self.jurisdiction = jurisdiction
        self.chamber = chamber
               
def serializing(obj):
    if isinstance(obj, Decision):
        return {
            "identifier": obj.identifier,
            "nb annotations":obj.nb_annotations,
            "jurisdiction": obj.jurisdiction,
            "chamber":obj.decision_chamber,
            "date": obj.date,
            "cassation id":obj.cassation_id,
            "ECLI":obj.ecli,
            "referral court": obj.referral_court,
            "appellants":obj.appellants,
            "defendants":obj.defendants,
            "legal references":obj.legal_references,
            "case law references":obj.case_law_references,
            "proceedings":obj.proceedings,
            "cassation appeals":obj.cassation_appeals,
            "second degree appeals":obj.appeals,
            "solution":obj.solutions,
            "unrecoverable costs":obj.unrecoverable_costs}
    if isinstance(obj, Proceeding):
        return {
            "date":obj.date,
            "event_type":obj.event_type,
            "jurisdiction":obj.jurisdiction,
            "chamber":obj.chamber,
            "start":obj.start}
    raise TypeError(repr(obj) + " n'est pas sérialisable !")

with open(filename,encoding="utf-8") as json_file:
    docs = json.load(json_file)
    for i in docs:
        #decisions metadata show up in the very first annotations
        jurisdiction = ""
        for j in i['annotations']:
            if j['labelName']=="juridiction":
                jurisdiction = j['text']
                break
        decision_chamber = ""
        for j in i['annotations']:
            if j['labelName']=="formation":
                decision_chamber = j['text']
                break
        date = ""
        for j in i['annotations']:
            if j['labelName']=="date_d_arret":
                date = j['text']
                break
        cassation_id = ""
        for j in i['annotations']:
            if j['labelName']=="numero_de_pourvoi":
                cassation_id = j['text']
                break
        ecli = ""
        for j in i['annotations']:
            if j['labelName']=="ecli":
                ecli = j['text']
                break
        referral_court = ""
        for j in i['annotations']:
            if j['labelName']=="juridiction_de_renvoi":
                referral_court = j['text']
                break
        decision = Decision(i['identifier'], 0, jurisdiction, decision_chamber, date, cassation_id, ecli, referral_court)
        date = ""
        event_type = ""
        jurisdiction = ""
        type = ""
        start=0
        nb_annotations=0
        for j in i['annotations']:
            nb_annotations +=1
            if (j['labelName'][0:4] == type) or ((j['labelName'][0:4] in ['juri','date']) and type != "" and j['start'] >= start+100): 
                if i['identifier'] == "ECLI-FR-CCASS-2020-C100616.txt":
                    print(str(j['start'])+";"+j['labelName']+";"+date+";"+event_type+";"+jurisdiction)
                decision.proceedings.append(Proceeding(start,date,event_type,jurisdiction,""))
                date = ""
                event_type = ""
                jurisdiction = ""
                type = ""
                start = j['start']
            if j['labelName'] in ["date_d_arret","date_de_jugement","date_de_refere","date_de_redressement_ou_liquidation"]:
                type = 'date'
                date = j['text'] 
                event_type = j['labelName']
                if i['identifier'] == "ECLI-FR-CCASS-2020-C100616.txt":
                    print(str(j['start'])+";"+j['labelName']+";"+date+";"+event_type+";"+jurisdiction)
                if jurisdiction != "" and j['start'] < start+100:
                    if i['identifier'] == "ECLI-FR-CCASS-2020-C100616.txt":
                        print(str(j['start'])+";"+j['labelName']+";"+date+";"+event_type+";"+jurisdiction)
                    decision.proceedings.append(Proceeding(start,j['text'],j['labelName'],jurisdiction,""))
                    date = ""
                    event_type = ""
                    jurisdiction = ""
                    type = ""
                start = j['start']
            elif j['labelName'] == "juridiction":
                type = 'juri'
                jurisdiction = j['text']
                if i['identifier'] == "ECLI-FR-CCASS-2020-C100616.txt":
                    print(str(j['start'])+";"+j['labelName']+";"+date+";"+event_type+";"+jurisdiction)
                if date != "" and j['start'] < start+100: 
                    decision.proceedings.append(Proceeding(start,date,event_type,j['text'],""))
                    date = ""
                    event_type = ""
                    jurisdiction = ""
                    type = ""
                start = j['start']
            elif j['labelName'] in ["date_de_mise_en_etat","date_d_assignation","date_expertise"]:
                if i['identifier'] == "ECLI-FR-CCASS-2020-C100616.txt":
                    print(str(j['start'])+";"+j['labelName']+";"+date+";"+event_type+";"+jurisdiction)
                date = j['text']
                event_type = j['labelName']
                decision.proceedings.append(Proceeding(j['start'],j['text'],j['labelName'],"",""))
            #one decision may have several parties, appeal numbers, legal references, case law references, even solutions
            elif j['labelName']=="demandeur":
                appellant = j['text']
                if appellant not in decision.appellants:
                    decision.appellants.append(appellant)
            elif j['labelName']=="defendeur":
                defendant = j['text']
                if defendant not in decision.defendants:
                    decision.defendants.append(defendant)                                        
            elif j['labelName']=="numero_de_pourvoi":
                cassation_id= j['text']
                if cassation_id not in decision.cassation_appeals:
                    decision.cassation_appeals.append(cassation_id)
            elif j['labelName']=="rg_appel":
                appeal_id = j['text']
                if appeal_id not in decision.appeals:
                    decision.appeals.append(appeal_id)
            elif j['labelName']=="reference_juridique":
                legal_reference= j['text'].replace(" et suivants","")
                if legal_reference not in decision.legal_references:
                    decision.legal_references.append(legal_reference)
                    #one single annotation may involve several articles from several codes or laws
                    position = 0
                    while position > -1:
                        position = legal_reference.find(",", position)
                        #print(i['identifier']+" ; "+legal_reference+str(legal_reference.find(" et ", position))+" ; "+str(legal_reference.find(",", position))+" ; "+str(position))
                        if position > -1:
                            decision.legal_references.append(legal_reference)
                            position +=1
                    position = 0
                    while position > -1:
                        position = legal_reference.find(" et ", position)
                        if position > -1:
                            decision.legal_references.append(legal_reference)
                            position +=1
            elif j['labelName'] =="reference_jurisprudentielle":
                case_law_reference = j['text']
                if case_law_reference not in decision.case_law_references:
                    decision.case_law_references.append(case_law_reference)
            elif j['labelName']=="condamne":
                solution = j['text']
                if solution not in decision.solutions:
                    decision.solutions.append(solution)
            #there may be several amounts, possibly identical, depending on which party pays which other party
            elif j['labelName']=="frais_irrepetibles":
                unrecoverable_cost = j['text']
                decision.unrecoverable_costs.append(unrecoverable_cost)                      
        #the decision is appended to other decisions already recorded
        decisions.append(decision)
        for k in decision.proceedings:
            for j in i['annotations']:
                if j['labelName'] == "formation" and j['start'] > k.start and j['start'] <= k.start+100:
                    k.chamber = j['text']
                    #print(str(k.start)+";"+k.jurisdiction+";"+k.date+";"+k.event_type+";"+str(j['start'])+";"+j['text'])
                    break
        #i['nb_annotations']= nb_annotations
        print(i['title']+" ; "+str(nb_annotations))
        nb_dec+=1
    print(str(nb_dec))
                     
with open('struc_'+filename, 'w', encoding='utf-8') as f:
    json.dump(decisions, f, default=serializing, indent=4,ensure_ascii=False)

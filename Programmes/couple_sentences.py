import json
import sys
filename = sys.argv[1]     
decisions = []
old_sentences = 0
new_sentences = 0
            
class Sentence:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
def serializing(obj):
    if isinstance(obj, Sentence):
        return {
            "start":obj.start,
            "end":obj.end}
            
with open(filename,encoding="utf-8") as json_file:
    docs = json.load(json_file)    
    for i in docs:
        status = "first"
        sentence_couples = []
        for j in i['sentences']:
            old_sentences +=1
            if status == "first":
                start= j['start']
                end = j['end']
                status = "second"
            else:
                end = j['end']
                sentence_couples.append(Sentence(start, end))
                new_sentences +=1
                status= 'first'
        #if there was an odd number of sentences, the last one is reproduced as it was
        if status == 'second':
            sentence_couples.append(Sentence(start, end))
            new_sentences +=1             
        i['sentences'] = sentence_couples              
        decisions += [i]
    print(old_sentences)
    print(new_sentences)
   
with open("coupled_"+filename, 'w', encoding='utf-8') as f:
    json.dump(decisions, f, default=serializing, indent=4,ensure_ascii=False)
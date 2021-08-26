import json
import sys
filename = sys.argv[1]       
total = 0

with open(filename, encoding="utf-8") as json_file:
    docs = json.load(json_file)    
    legal_references = []
    for i in docs:
        decision=0
        position = ""
        for j in i['annotations']:
            if j['labelName']== "article":
                legal_reference= i['identifier']+";"+j['text']
                position = "article"
            elif position == "article" and legal_reference+";"+j['text'] not in legal_references:
                legal_references.append(legal_reference+";"+j['text'])
                position = "instrument"
                decision+=1
                total+=1               

with open("obtained_results.txt", "w", encoding="utf-8") as out:
    for i in legal_references:
        out.write("%s" % (i))
        out.write("\n")
    out.close()
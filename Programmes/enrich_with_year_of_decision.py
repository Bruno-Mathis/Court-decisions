import sys
import json
filename = sys.argv[1]
with open(filename,encoding="utf-8") as json_file:
    docs = json.load(json_file)
    decisions = []
    for i in docs:
        year = 0
        for j in i['annotations']:
            if j['labelName'] in ['date_de_jugement','date_d_arret','date_de_refere', 'date_de_mise_en_etat']:             
                try:
                    year = int(j['text'][len(j['text'])-4:len(j['text'])])
                    i['metadata']['Année'] = year
                    break
                except ValueError :
                    print(i['identifier']+";"+j['labelName']+";"+j['text'])
        decisions += [i]

with open("with_year_"+filename, 'w', encoding='utf-8') as f:
    json.dump(decisions, f, indent=4,ensure_ascii=False)

import sys
import json
filename = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3]
with open(filename,encoding="utf-8") as json_file:
    docs = json.load(json_file)
    decisions = []
    for i in docs:
        if 'Année' in i['metadata']:
            if int(i['metadata']['Année']) >= int(start) and int(i['metadata']['Année']) <= int(end):
                    decisions += [i]

with open("from_"+start+"_to_"+end+"_"+filename, 'w', encoding='utf-8') as f:
    json.dump(decisions, f, indent=4,ensure_ascii=False)

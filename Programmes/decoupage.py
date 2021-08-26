#creates one txt file per individual decisionimport sys
filename = sys.argv[1]
fid = open(filename,encoding="utf-8")
dbstr = fid.read()
longueur = len(dbstr)
fid.close()
start=5
counter=0
while start < longueur:
    next = dbstr.find("#####",start)
    if next ==-1:
        decision = dbstr[start:]
        identifier = decision[0:20]
        counter+=1
        output = open(str(counter)+'-'+identifier+'.txt','w',encoding="utf-8")
        output.write(decision)
        output.close()
        break
    decision = dbstr[start:next]
    identifier = decision[0:20]
    counter+=1
    output = open(str(counter)+'-'+identifier+'.txt','w',encoding="utf-8")
    output.write(decision)
    output.close()
    start=next+5

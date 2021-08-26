import os
import json
import sys

class DBDict():
    def __init__(self,filename):
        self.DBDict = dict()
        self.dbname = filename
        self.debug("DBDict - init - dbname : "+self.dbname)
        if os.path.exists(self.dbname):
            fid = open(self.dbname,encoding="utf-8")
            dbstr = fid.read()
            fid.close()
            self.DBDict = json.loads(dbstr)
            self.debug("__init__ dbstr : " + dbstr)
            self.debug("__init__ DBDict :" + str(self.DBDict))
    
    def processing(self):
        extractions = []
        nb_decisions=0
        nb_segments=0
        for i in self.DBDict:
             for j in i['annotations']:
                if j['labelName'] == "matiere" and j['text'] == matter:
                    extractions.append([i])
                    nb_decisions+=1
                    for s in i['sentences']:
                        nb_segments+=1
        full_str = json.dumps(extractions,indent=4,ensure_ascii=False)
        print(str(nb_decisions)+" documents")
        print(str(nb_segments)+" segments")
        fid = open(matter+"_"+self.dbname,"w",encoding="utf-8")
        fid.write(full_str)
        fid.close()

    def debug(self,message):
        if False:
            print("Common.py DBDict - " + message)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        matter = sys.argv[2]
        dbdict = DBDict(filename)
        dbdict.processing()

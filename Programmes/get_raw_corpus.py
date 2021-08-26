#this program builds a corpus free from manual annotations so as to have it trained through Sherpa's API
import os
import sys
import json
class DBDict():
    def __init__(self,filename):
        self.DBDict = dict()
        # So DBDict should be
        self.dbname = 'clean_'+filename
        self.debug("DBDict - init - dbname : "+self.dbname)
        # loading
        if os.path.exists(self.dbname):
            input_file = open(self.dbname,encoding="utf-8")
            dbstr = input_file.read()
            input_file.close()
            self.DBDict = json.loads(dbstr)
            self.debug("__init__ dbstr : " + dbstr)
            self.debug("__init__ DBDict :" + str(self.DBDict))
        decisions = []
        #for each decision, identifier and text only are kept
        for i in self.DBDict:
            decisions.append({'identifier':i['identifier'],'text':i['text']})
        new_str = json.dumps(decisions,indent=4)
        new_str = new_str.replace("Ï","")
        output_file = open("raw_"+filename, "w", encoding="utf-8")
        output_file.write(new_str)
        output_file.close()
        
    def debug(self,message):
        if False:
            print("Common.py DBDict - " + message)
            
if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        dbdict = DBDict(filename)

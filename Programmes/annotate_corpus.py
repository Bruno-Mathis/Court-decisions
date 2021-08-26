import os
import json
import requests
import sys
import time

server        = 'https://sherpa-gpu.kairntech.com/api'
login_info    = json.dumps({"email": 'bmathis', "password": 'Azanie34!'})
headers = {"Accept": "application/json", "Content-Type": "application/json"}

def get_token(server, login_info):
    url = server + "/auth/login"
    #print("calling sherpa server '%s' ..." % url)
    try:
        response = requests.post(url,data=login_info, headers=headers)
        json_response = json.loads(response.text)
    except Exception as ex:
        print("Error connecting to Sherpa server %s: %s" % (server, ex))
        return 
    #print("response = %s" % response.text)
    if 'access_token' in json_response:
        token = json_response['access_token']
        return token
    else:
        return 

def call_sherpa(id, text,model,annotator,server,token,chunklength=10000000):
    url = server + "/projects/" + model + "/annotators/" + annotator + "/_annotate"
    #print("calling sherpa server '%s' ... " % url)
    text = text.encode(encoding='utf-8')
    headers = {"Accept": "application/json",
               "Content-Type": "text/plain",
               "Authorization": "Bearer " + token}
    response = requests.post(url,data=text, headers=headers)
    if (response.status_code != 200):
        print("error from server: %s for document: %s" % (response.status_code, id))
        return response.status_code
    else:
        return response.text
    return result
    
class DBDict():
    def __init__(self,filename):
        self.DBDict = dict()
        self.dbname = filename
        self.debug("DBDict - init - dbname : "+self.dbname)
        if os.path.exists(self.dbname):
            input_file = open(self.dbname,encoding="utf-8")
            dbstr = input_file.read()
            input_file.close()
            self.DBDict = json.loads(dbstr)
            self.debug("__init__ dbstr : " + dbstr)
            self.debug("__init__ DBDict :" + str(self.DBDict))

    def debug(self,message):
        if False:
            print("Common.py DBDict - " + message)
        
if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        project = sys.argv[2]
        experience = sys.argv[3]
        token = get_token(server,login_info)
        input_file = open(filename,encoding="utf-8")
        text = input_file.read()
        jsoncontent = json.loads(text)
        input_file.close()
        list_of_decisions = []
        for doc in jsoncontent:
            id   = doc['identifier']
            text = doc['text']  
            list_of_decisions += [(id,text)]
        output = ""
        counter = 0        
        for decision in list_of_decisions:
            id   = decision[0]
            text = decision[1]
            start_time = time.time()
            result = call_sherpa(id,text,project,experience,server,token,chunklength=10000000)
            #we compute runtime on a single decision
            runtime = time.time() - start_time
            #if the requests function sent an error code, the decision is disregarded and the parsing stops
            if type(result) == int:
                break
            else:
                counter += 1
                print("Décision: %s %s annotée en %s secondes" % (counter,id,runtime))
                #inserting the identifier metadata at start of each decision
                result = result.replace('{\n  "text" :','{\n  "identifier" : "'+id+'",\n'+'  "text" :')
                #adding a document comma delimiter
                result += ","
                output += result
        output_file = open(experience+"_"+filename, 'w', encoding = "utf-8")
        output = "[\n"+output+"\n]"
        output = output.replace(",\n]","\n]").replace("","").replace("","s").replace("”","").replace("“","").replace("Ï","I").replace("❖","").replace("✏","")      
        output_file.write(output)
        output_file.close()
        print("output written to %s" % experience+"_"+filename) 

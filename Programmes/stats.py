import sys
import json
import statistics
filename = sys.argv[1]
fid = open(filename,encoding="utf-8")
dbstr = fid.read()
decisions = json.loads(dbstr)
stats = open('stats_'+filename+'.csv','w',encoding="utf-8")
stats.write("identifier;title;jurisdiction;date;length;nb annotations;nb segments;avg size;std dev size;min size;max size")
stats.write("\n")
for i in decisions:
    nb_anno = 0
    nb_segments = 0
    min =-1
    max =-1
    length = len(i['text'])
    seg_lengths = []
    for j in i['sentences']:
        seg_length = j['end']-j['start']
        seg_lengths.append(seg_length)
        if seg_length < min or min==-1:
            min = seg_length
        if seg_length > max or max==-1:
            max = seg_length
        nb_segments+=1
    if nb_segments > 1:
        stdev_segments = round(statistics.stdev(seg_lengths))
    else:
        stdev_segments = 0
    jur_indicator = False
    date_indicator = False
    date=""
    for j in i['annotations']:
        nb_anno+=1
        if j['labelName']=="juridiction" and jur_indicator is False:
            jur_indicator = True
            jurisdiction = j['text'].replace('\n', ' ').replace("\t", " ").replace(";", " ").replace(",","-")
        if j['labelName']=="date_d_arret" and date_indicator is False:
            date_indicator = True
            date = j['text']
        elif j['labelName']=="date_de_jugement" and date_indicator is False:
            date_indicator = True
            date = j['text']	
    decision = i['identifier']+";"+i['title']+";"+jurisdiction+";"+date+";"+str(length)+";"+str(nb_anno)+";"+str(nb_segments)+";"+str(round(length/nb_segments))+";"+str(stdev_segments)+";"+str(min)+";"+str(max)
    stats.write(decision)
    stats.write("\n")
stats.close()
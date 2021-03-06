import requests
from bs4 import BeautifulSoup

res = requests.get('https://tv.naver.com/r')
raw = res.text
html = BeautifulSoup(raw,'html.parser')

clips = html.select('dl.cds_info')

info = {}

for clip in clips:
    chn = clip.select_one('dd.chn').text.strip()
    hit = int(clip.select_one('span.like').text.replace(',','')[5:])
    like = int(clip.select_one('span.hit').text.replace(',','')[6:])
    score = hit + like*350/100
    if chn in info.keys():
        info[chn]['hit'] += hit
        info[chn]['like'] += like
        info[chn]['score'] += score
    else:
        info[chn] = {'hit':hit,'like':like,'score':score}

def sort_by_score(item):
    return item[1]['score']

f = open('2_txt.txt','w',encoding='utf8')
for arg in sorted(info.items() , key = sort_by_score , reverse=True):
    f.write(arg[0]+
        str(arg[1]['hit'])+','+str(arg[1]['like'])+','+str(arg[1]['score'])+'\n')

f.close()

f = open('2_csv.csv','w',encoding='utf8')
for arg in sorted(info.items() , key = sort_by_score , reverse=True):
    f.write(arg[0]+
        str(arg[1]['hit'])+','+str(arg[1]['like'])+','+str(arg[1]['score'])+'\n')

f.close()

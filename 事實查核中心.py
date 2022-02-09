import requests 
from bs4 import BeautifulSoup
import re 
import pandas as pd

class Crawler_FactCheck():
    def __init__(self,baseUrl):
        self.url = baseUrl
        self.target = pd.DataFrame({'Label':[],'CSS':[]})
    
    def GetLatestId(self):
        x = requests.get(self.url)
        self.content = BeautifulSoup(x.content.decode('utf-8'),'lxml')
        latest = self.content.select('.entity-list-title a')[0]['href']
        self.latestId = re.findall('[0-9]+',latest)[0]
        del x,latest
    
    def AddTargetCSS(self,**kwargs):
        for k,v in kwargs.items():
            self.target = self.target.append({'Label':k,'CSS':v},ignore_index=True)
            self.target.drop_duplicates(inplace=True)
        
    def GetData(self,nums):
        Labels = self.target['Label'].values.tolist()
        Css = self.target['CSS'].values.tolist()
        self.df = pd.DataFrame()
        for i in range(len(Css)):
            globals()['var'+str(i)] = []
        for minus in range(nums):
            r = requests.get(f'https://tfc-taiwan.org.tw/articles/{int(self.latestId)-minus}')
            if r.status_code != 200:
                print(f"")
                continue
            resp = BeautifulSoup(r.content.decode('utf-8'),'lxml')
            for i in range(len(Css)):
                print(Labels[i],[i.text.strip() for i in resp.select(Css[i]) ])
                globals()['var'+str(i)].append( resp.select(Css[i])[-1].text.strip() )
        self.df = pd.DataFrame(dict(zip(Labels,[ eval('var'+str(i)) for i in range(len(Labels))])))
        
            



new = Crawler_FactCheck('https://tfc-taiwan.org.tw/articles/report')
new.GetLatestId()
new.AddTargetCSS(true='#block-system-main .odd a',category='.field-type-taxonomy-term-reference .even a',
                title='#block-system-main .node-title',date='#block-system-main .submitted')
new.GetData(10)
new.df

x = requests.get('https://tfc-taiwan.org.tw/articles/report')
resp = BeautifulSoup(x.text,'lxml')
resp.select('#block-system-main .last a')[0]['href']
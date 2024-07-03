import os
import sys

from dotenv import load_dotenv
from pymongo import MongoClient
import json


MONGODB_URI = os.environ.get('MONGODB_URI')
years= ["2020","2021","2022"]
months = ['01','02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
path = "D:\Carrera\TFG\Pruebas de código\Pruebas OpenAI\ProcessedNews"
newsPapers = ["ElDiario","ElMundo","ElPais","LibertadDigital"]
pathNews = ["/Eldiario","/ElMundo", "/ElPais", "/LibertadDigital"]

client = MongoClient(MONGODB_URI)

for pathNew, newsPaper in zip(pathNews,newsPapers):
    db = client[f'PRO-{newsPaper}']
    for y in  years:
        for m in months:
            if f'{y}-{m}' == '2022-03' and newsPaper == 'LibertadDigital':
                sys.exit()
            collection = db[f'PRO-Noticias_{y}-{m}']
            file = f'{path}{pathNew}/PRO-Noticias_{y}-{m}.json'
            with open(file, 'r', encoding='utf-8') as f:
                news = json.load(f)
            collection.insert_many(news)
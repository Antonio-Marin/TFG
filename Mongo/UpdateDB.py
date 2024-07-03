# DON'T FORGET TO RUN THE VIRTUAL ENVIRONMENT FIRST!
# .\mongo-env\Scripts\activate
import os
import sys

from dotenv import load_dotenv
from pymongo import MongoClient
import json


MONGODB_URI = os.environ.get('MONGODB_URI')
years= ["2020","2021","2022"]
months = ['01','02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
path = "D:/Carrera/TFG/Pruebas de código/Extraccion/jsons"
#pathNews = ["/El diario/order","/El Mundo", "/El Pais/ELPAISV3", "/Libertad digital"]
pathNews = ["/El diario/order"]
# newsPapers = ["ElDiario","ElMundo","ElPais","LibertadDigital"]
newsPapers = ["ElDiario"]

client = MongoClient(MONGODB_URI)
for pathNew, newsPaper in zip(pathNews,newsPapers):
    db = client[newsPaper]
    for y in  years:
        for m in months:
            if f'{y}-{m}' == '2022-03' and newsPaper == 'LibertadDigital':
                sys.exit()
            collection = db[f'Noticias_{y}-{m}']
            file = f'{path}{pathNew}/datos_{y}-{m}.json'
            with open(file, 'r', encoding='utf-8') as f:
                news = json.load(f)
                if newsPaper == "ElPais" or newsPaper== 'ElDiario':
                    collection.insert_many(news)

                elif newsPaper == "ElMundo":
                    newsList = []
                    for new in news:
                        newsDict = dict()
                        newsDict['Título'] = new['Tema'].strip()+new['Título'].strip()
                        newsDict['Cuerpo'] = new['Cuerpo'].strip()
                        newsDict['Enlace'] = new['Enlace']
                        newsList.append(newsDict)
                    collection.insert_many(newsList)
                else:
                    newsList = []
                    for new in news:
                        newsDict = dict()
                        newsDict['Titulo'] = new['Título'].strip()
                        if not 'Cuerpo' in new:
                            newsDict['Cuerpo'] = "Error al obtener el contenido"
                        else:
                            newsDict['Cuerpo'] = new['Cuerpo'].strip()
                        newsDict['Enlace'] = new['Enlace']
                        newsList.append(newsDict)
                    collection.insert_many(newsList)




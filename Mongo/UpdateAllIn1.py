import os
import sys
import json
from pymongo import MongoClient

# Configurar URI de MongoDB
MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)

years = ["2020", "2021", "2022"]
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
path = "D:/Carrera/TFG/Pruebas de código/Pruebas OpenAI/ProcessedNews"
newsPapers = ["ElDiario", "ElMundo", "ElPais", "LibertadDigital"]
pathNews = ["/Eldiario", "/ElMundo", "/ElPais", "/LibertadDigital"]

skip_to_saving = False

# Lista para almacenar todas las noticias
all_news = []

for pathNew, newsPaper in zip(pathNews, newsPapers):
    for y in years:
        for m in months:
            if f'{y}-{m}' == '2022-03' and newsPaper == 'LibertadDigital':
                skip_to_saving = True
                break
            file = f'{path}{pathNew}/PRO-Noticias_{y}-{m}.json'
            if os.path.exists(file):
                with open(file, 'r', encoding='utf-8') as f:
                    news = json.load(f)
                    all_news.extend(news)
        if skip_to_saving:
            break
    if skip_to_saving:
        break
                

# Guardar todas las noticias en un solo archivo JSON
combined_news_file = 'combined_news.json'
with open(combined_news_file, 'w', encoding='utf-8') as f:
    json.dump(all_news, f, ensure_ascii=False, indent=4)

print(f'Todas las noticias han sido combinadas en {combined_news_file}')

# Subir los datos combinados a MongoDB
db = client['All-PRO']
collection = db['PRO-Noticias']

with open(combined_news_file, 'r', encoding='utf-8') as f:
    combined_news = json.load(f)

collection.insert_many(combined_news)

print('Todas las noticias combinadas han sido subidas a MongoDB')

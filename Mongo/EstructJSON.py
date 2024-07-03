# DON'T FORGET TO RUN THE VIRTUAL ENVIRONMENT FIRST!
# .\mongo-env\Scripts\activate
import os
import re
import sys
from pymongo import MongoClient

years= ["2020","2021","2022"]
months = ['01','02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#datePattern= r"/(\d{4})/(\d{2})/(\d{2})/" #El Mundo
datePattern = r"/(\d{4})-(\d{2})-(\d{2})/" # Para el formato "YYYY-MM-DD"

#TODO: Obtain JSONS from MongoDB
MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client["LibertadDigital"]

for y in  years:
    for m in months:
        if f'{y}-{m}' == '2022-03':
                sys.exit()
        collection = db[f'Noticias_{y}-{m}']
        news = collection.find()

        for new in news:
            if new["Cuerpo"] == "Error al obtener el contenido":
                collection.delete_one({"_id": new["_id"]})
            else:
                link = new["Enlace"]
                result = re.search(datePattern, link)
                if result:
                    year = result.group(1)
                    month = result.group(2)
                    day = result.group(3)
                    date = f"{day}/{month}/{year}"
                    collection.update_one({"_id": new["_id"]}, {"$set": {"Fecha": date}})
                else:
                    collection.delete_one({"_id": new["_id"]})

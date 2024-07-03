# DON'T FORGET TO RUN THE VIRTUAL ENVIRONMENT FIRST!
# .\mongo-env\Scripts\activate
import os
import sys
import re

from dotenv import load_dotenv
from pymongo import MongoClient
import json

years= ["2020","2021","2022"]
months = ['01','02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
path = "D:/Carrera/TFG/Pruebas de código/Extraccion/jsons/El Pais/ELPAISV3"

datePattern = r"/(\d{4})/(\d{2})/(\d{2})/"
datePattern2 = r"/(\d{4})-(\d{2})-(\d{2})/"

MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client["ElPais"]

for y in  years:
    for m in months:
        collection = db[f'Noticias_{y}-{m}']
        for news in collection.find():
            link = news["Enlace"]
            date = news.get("Fecha", "Fecha por estimar")
            body = news.get("Cuerpo", "")

            if body == "Error al obtener el contenido":
                print(f"Borrando noticia: {link} debido a un error al obtener el contenido.")
                collection.delete_one({"_id": news["_id"]})
                continue

                # Si la fecha es "Mal" o introducida manualmente como "Mal", borramos la noticia
            if date == "Mal":
                print(f"Borrando noticia: {link} debido a una fecha incorrecta.")
                collection.delete_one({"_id": news["_id"]})
                continue
            
            # Si la fecha es "Fecha por estimar", solicitamos una nueva fecha
            if date == "Fecha por estimar":
                print(f"El enlace {link} no tiene fecha estimada.")
                nueva_fecha = input("Ingresa la nueva fecha (formato dd-mm-yyyy), o 'Mal' para borrar la noticia: ")
                
                # Si la fecha ingresada manualmente es "Mal", borramos la noticia
                if nueva_fecha.lower() == "mal":
                    print(f"Borrando noticia: {link} debido a una fecha incorrecta.")
                    collection.delete_one({"_id": news["_id"]})
                else:
                    # Actualizamos el documento con la nueva fecha
                    collection.update_one({"_id": news["_id"]}, {"$set": {"Fecha": nueva_fecha}})
                    print(f"La fecha del enlace {link} ha sido actualizada a {nueva_fecha}")
        # file = f'{path}/datos_{y}-{m}.json'
        # with open(file, 'r', encoding='utf-8') as f:
        #         news_list = json.load(f)
        # for news in news_list:
        #     link = news["Enlace"]
        #     result = re.search(datePattern, link)
        #     result2 = re.search(datePattern2, link)
        #     if result:
        #         year = result.group(1)
        #         month = result.group(2)
        #         day = result.group(3)
        #         date = f"{day}-{month}-{year}"
        #         news["Fecha"] = date
        #     elif result2:
        #         year = result2.group(1)
        #         month = result2.group(2)
        #         day = result2.group(3)
        #         date = f"{day}-{month}-{year}"
        #         news["Fecha"] = date
        #     else:
        #         news["Fecha"] = "Fecha por estimar"

        # collection.insert_many(news_list)
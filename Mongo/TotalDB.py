# DON'T FORGET TO RUN THE VIRTUAL ENVIRONMENT FIRST!
# .\mongo-env\Scripts\activate

from pymongo import MongoClient
import os

MONGODB_URI = os.environ.get('MONGODB_URI')
db_names = ["ElMundo","ElPais","LibertadDigital", "ElDiario"]

totalNews = 0
totalWithoutBody = 0
newsElPais = 0
newsElPaisWOB = 0
newsElMundo = 0
newsElMundoWOB = 0
newsLibertadDigital = 0
newsLibertadDigitalWOB = 0
newsElDiario = 0
newsElDiarioWOB = 0

client = MongoClient(MONGODB_URI)
for db_name in db_names:
    db = client[db_name]
    collections = db.list_collection_names()
    for collection_name in collections:
        count = db[collection_name].count_documents({})
        conteo = db[collection_name].count_documents({"Cuerpo": "Error al obtener el contenido"})
        if db_name == "ElPais":
            newsElPais+=count
            newsElPaisWOB+=conteo
        elif db_name == "ElMundo":
            newsElMundo+=count
            newsElMundoWOB+=conteo
        elif db_name== "LibertadDigital":
            newsLibertadDigital+=count
            newsLibertadDigitalWOB+=conteo
        else:
            newsElDiario += count
            newsElDiarioWOB += conteo

        totalNews += count
        totalWithoutBody += conteo

print("Hay ", totalNews, " noticias en la BBDD.")
print(newsElPais," noticias pertenecen a El País.")
print(newsElDiario," noticias pertenecen a El Diario.")
print(newsElMundo," noticias pertenecen a El Mundo.")
print(newsLibertadDigital," noticias pertenecen a Libertad Digital.")
print("-----------------------------------------------")
print("Hay ", totalWithoutBody, "  noticias sin cuerpo en la BBDD.")
print(newsElPaisWOB," noticias sin cuerpo pertenecen a El País.")
print(newsElDiarioWOB," noticias sin cuerpo pertenecen a El Diario.")
print(newsElMundoWOB," noticias sin cuerpo pertenecen a El Mundo.")
print(newsLibertadDigitalWOB," noticias sin cuerpo pertenecen a Libertad Digital.")
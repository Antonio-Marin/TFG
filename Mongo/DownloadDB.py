from pymongo import MongoClient
import os
import json

MONGODB_URI = os.environ.get('MONGODB_URI')
db_names = ["ElMundo", "ElPais", "ElDiario", "LibertadDigital"]

client = MongoClient(MONGODB_URI)
for db_name in db_names:
    db = client[db_name]
    collections = db.list_collection_names()
    for collection_name in collections:
        collection = db[collection_name]
        documents = collection.find()
        json_data = []
        for doc in documents:
            del doc['_id']
            json_data.append(doc)

        pathJson = f'D:\Carrera\TFG\Pruebas de código\Mongo\DB\{db_name}\{collection_name}.json'
        with open(pathJson, 'w', encoding='utf-8') as jsonFile:
            json.dump(json_data, jsonFile, ensure_ascii=False, indent=4)

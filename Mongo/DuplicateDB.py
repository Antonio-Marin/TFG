from pymongo import MongoClient
import os

# Conectar a la base de datos
MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db_names1 = ["ElPais", "ElDiario"]
db_names2 = ["ElMundo", "LibertadDigital"]

print(db_names1)
print("====================================================================")
for db_name in db_names1:
    db = client[db_name]
    print("-------------------------")
    print(db_name)
    print("-------------------------")
    collections = db.list_collection_names()
    for collection_name in collections:
        collection = db[collection_name]  # Obtener la colección utilizando el nombre
        # Identificar un campo único para determinar la duplicación de las noticias (por ejemplo, '_id')
        pipeline = [
            {
                '$group': {
                    '_id': '$Título', 
                    'count': {'$sum': 1},
                    'docs': {'$push': '$_id'}  # Agregar IDs a la lista 'docs'
                }
            },
            {
                '$match': {
                    'count': {'$gt': 1}  # Filtrar las noticias que aparecen más de una vez (duplicadas)
                }
            }
        ]

        # Ejecutar la agregación
        result = list(collection.aggregate(pipeline))

        if result:
            print(db_name,"Noticias duplicadas en la colección", collection_name)
            for doc in result:
                print(f"{doc['_id']}: {doc['count']} veces.")
                # Eliminar las noticias duplicadas
                # duplicated_ids = doc['docs'][1:]  # Ignorar el primer ID
                # collection.delete_many({'_id': {'$in': duplicated_ids}})
        else:
            print("No hay noticias duplicadas en la colección", collection_name)

print("====================================================================")
print(db_names2)
print("====================================================================")
for db_name in db_names2:
    db = client[db_name]
    print("-------------------------")
    print(db_name)
    print("-------------------------")
    collections = db.list_collection_names()
    for collection_name in collections:
        collection = db[collection_name]  # Obtener la colección utilizando el nombre
        # Identificar un campo único para determinar la duplicación de las noticias (por ejemplo, '_id')
        pipeline = [
            {
                '$group': {
                    '_id': '$Titulo',  # Reemplaza 'campo_unico' por el nombre de tu campo único
                    'count': {'$sum': 1}
                }
            },
            {
                '$match': {
                    'count': {'$gt': 1}  # Filtrar las noticias que aparecen más de una vez (duplicadas)
                }
            }
        ]

        # Ejecutar la agregación
        result = list(collection.aggregate(pipeline))

        if result:
            print(db_name,"Noticias duplicadas en la colección", collection_name)
            for doc in result:
                print(f"{doc['_id']}: {doc['count']} veces.")
        else:
            print("No hay noticias duplicadas en la colección", collection_name)

# from pymongo import MongoClient
# import os

# # Conectar a la base de datos
# MONGODB_URI = os.environ.get('MONGODB_URI')
# client = MongoClient(MONGODB_URI)

# # Diccionario para almacenar las noticias duplicadas
# duplicated_news = {}

# for db_name in db_names2:
#     db = client[db_name]
#     collections = db.list_collection_names()
#     for collection_name in collections:
#         collection = db[collection_name]
#         pipeline = [
#             {
#                 '$group': {
#                     '_id': '$Titulo',  # Campo único para identificar las noticias
#                     'count': {'$sum': 1}
#                 }
#             },
#             {
#                 '$match': {
#                     'count': {'$gt': 1}  # Filtrar las noticias que aparecen más de una vez (duplicadas)
#                 }
#             }
#         ]
#         result = list(collection.aggregate(pipeline))
#         for doc in result:
#             title = doc['_id']
#             count = doc['count']
#             if title not in duplicated_news:
#                 duplicated_news[title] = {'collections': [], 'count': count}
#             duplicated_news[title]['collections'].append((db_name, collection_name))

# # Imprimir las noticias duplicadas y en qué colecciones se encuentran
# for title, info in duplicated_news.items():
#     print(f"Título: {title}, Duplicado en:")
#     for collection_info in info['collections']:
#         db_name, collection_name = collection_info
#         print(f"- Colección {collection_name} de la base de datos {db_name}")

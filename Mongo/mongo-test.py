from pymongo import MongoClient
import os
import warnings
from cryptography.utils import CryptographyDeprecationWarning

#Para ignorar el warning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)

db = client['All-PRO']
collection = db['PRO-Noticias']
print(collection.count_documents({}))
documents = collection.find()
for document in documents:
    print(document['_id'])
# ids = collection.find({}, {"_id": 1}) #El 1 para que solo incluya el id, si pones el 0 incluye todos los datos menos el id
# for document in ids:
#     print(document["_id"])
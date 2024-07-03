
import datetime
import os

from dotenv import load_dotenv
#Ejecuta el entorno virtual
from pymongo import MongoClient
from pprint import pprint

MONGODB_URI = os.environ.get('MONGODB_URI')

# Connect to your MongoDB cluster:
client = MongoClient(MONGODB_URI)

# print('List all the databases in the cluster:')
# for db_info in client.list_database_names():
#    print(db_info)

# Get a reference to the 'sample_mflix' database:
db = client['sample_mflix']
# print('\n')

# print('List all the collections in sample_mflix:')
# collections = db.list_collection_names()
# for collection in collections:
#    print(collection)

# Get a reference to the 'movies' collection:
movies = db['movies']

# Get the document with the title 'The Iron Horse':
pprint(movies.find_one({'title': 'The Iron Horse'}))
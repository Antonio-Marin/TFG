from openai import Client
import os
from tqdm import tqdm

from pymongo import MongoClient
import warnings
from cryptography.utils import CryptographyDeprecationWarning

from pinecone.grpc import PineconeGRPC as Pinecone

# -------------MONGO-------------

#Para ignorar el warning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

MONGODB_URI = os.environ.get('MONGODB_URI')

def load_one_new():
    client = MongoClient(MONGODB_URI)
    db = client['All-PRO']
    collection = db['PRO-Noticias']

    return collection.find_one()


# -----------EMBEDDINGS-----------

openai_key = os.environ.get('OPENAI_API_KEY')
client = Client(api_key=openai_key)

EMBEDDING_MODEL = "text-embedding-3-small"

def get_embedding(text):
    if not text or not isinstance(text, str):
        return None
    try:
        response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        print(f"Error in get_embedding: {e}")
        return None

new_data = load_one_new()

print(new_data)

# Extraemos los datos para despues crear el embedding
redaction_date = new_data.get('fecha_redaccion', '')
active_subject = new_data.get('sujeto_activo', '')
object_part = new_data.get('parte_objeto', '')
main_topic = new_data.get('tema_principal', '')
tone = new_data.get('tono', '')
summary = new_data.get('resumen', '')
keywords = new_data.get('palabras_clave', [])
statements = new_data.get('declaraciones', [])

# Concateno
processed_text = f"{redaction_date} {active_subject} {object_part} {main_topic} {tone} {summary} {' '.join(keywords)} {' '.join([dec['declaracion'] for dec in statements if 'declaracion' in dec])}"

# # print(processed_text)

if processed_text:
    embedding = get_embedding(processed_text)
    if embedding:
        output = dict()
        output['id'] = new_data['_id']
        output['embedding'] = embedding
        # print(output)
    else:
        print(f"Failed to generate embedding for the processed news item: {processed_text}")
else:
    print(f"Processed text is empty for the news")

#-----------PINECONE-----------
pinecone_key = os.environ.get('PINECONE_API_KEY')
pc = Pinecone(api_key=pinecone_key)

index_name = 'news'

index = pc.Index(index_name)

if output['embedding']:
    objectId = str(output['id'])
    embedding = list(output['embedding'])
    index.upsert([(objectId, embedding)])

print(index.describe_index_stats())

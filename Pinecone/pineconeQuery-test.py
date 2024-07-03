from openai import Client
from pinecone.grpc import PineconeGRPC as Pinecone
import os
import json

pinecone_key = os.environ.get('PINECONE_API_KEY')
pc = Pinecone(api_key=pinecone_key)

openai_key = os.environ.get('OPENAI_API_KEY')
client = Client(api_key=openai_key)
EMBEDDING_MODEL = "text-embedding-3-small"

index_name = 'news'
index = pc.Index(index_name)

def load_json_files(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

filepath = 'D:\Carrera\TFG\Pruebas de código\Pruebas OpenAI\EMB-NewsTest.json'
news_data = load_json_files(filepath)

def get_embedding(text):
    try:
        response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        print(f"Error in get_embedding: {e}")
        return None

def search_in_pinecone(query, top_k=5):
    query_embedding = get_embedding(query)
    if query_embedding:
        query_response = index.query(vector=query_embedding, top_k=top_k)
        return query_response['matches']
    else:
        print("Failed to generate embedding for the query.")
        return []
    
def get_original_data_by_id(data, vector_id):
    index = int(vector_id.split('-')[1])
    return data[index]

query = "Noticias con un tono Neutral"
results = search_in_pinecone(query)

for index, result in enumerate(results, start=1):
    original_data = get_original_data_by_id(news_data, result['id'])

    output_filepath = f'D:\Carrera\TFG\Pruebas de código\Pruebas OpenAI\Pruebas Query-Pinecone\RESULTP-NewsTest{index}.json'
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(original_data, f, ensure_ascii=False, indent=2)
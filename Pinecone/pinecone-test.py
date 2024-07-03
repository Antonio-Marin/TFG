from pinecone.grpc import PineconeGRPC as Pinecone
import os
import json

api_key = os.environ.get('PINECONE_API_KEY')
pc = Pinecone(api_key=api_key)

# Nombre del índice
index_name = 'news'

# Conectar al índice
index = pc.Index(index_name)

# Función para cargar y procesar el JSON
def load_json_files(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Cargar datos del archivo JSON
filepath = 'D:\Carrera\TFG\Pruebas de código\Pruebas OpenAI\EMB-NewsTest.json'
news_data = load_json_files(filepath)
print(news_data)

# Insertar datos en Pinecone
for i, item in enumerate(news_data):
    if item['embedding']:  # Comprobación de que el campo embedding no esta vacio
        vector_id = f"news-{i}"  # Id para acda evctor
        index.upsert([(vector_id, item['embedding'])])

# Verificar que los datos se han insertado correctamente
print(index.describe_index_stats())

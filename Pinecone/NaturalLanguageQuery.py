from pymongo import MongoClient
from bson.objectid import ObjectId
from openai import Client
from pinecone.grpc import PineconeGRPC as Pinecone
import os
import warnings
from cryptography.utils import CryptographyDeprecationWarning

class Program():

    #TODO: hacer nuevo prompt para sacar conclusiones de request (query lenguaje natural + noticias obtenidas)
    #TODO: usar GPT4o-mini
    #TODO: implementar gradio

    def __init__(self):
        # Ignore warning
        warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

        # Mongo variables
        MONGODB_URI = os.environ.get('MONGODB_URI')
        self.mongoClient = MongoClient(MONGODB_URI)

        # OPENAI variables
        OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
        self.openAiClient = Client(api_key=OPENAI_KEY)
        self.EMBEDDING_MODEL = "text-embedding-3-small"

        # Pinecone variables
        PINECONE_KEY = os.environ.get('PINECONE_API_KEY')
        pc = Pinecone(api_key=PINECONE_KEY)
        
        index_name = 'news'
        self.index = pc.Index(index_name)

        # EXECUTION
        self.run()

    def run(self):
        print('Introduce your query in natural language:')
        query = input()
        results = self.searchInPinecone(query)
        articlesData = self.getArticles(results)
        request = self.processArticles(articlesData, query)
        print(request)

    def searchInPinecone(self, query, top_k=5):
        queryEmbedding = self.getEmbedding(query)
        if queryEmbedding:
            query_response = self.index.query(vector=queryEmbedding, top_k=top_k)
            return query_response['matches']
        else:
            print("Failed to generate embedding for the query.")
            return []

    def getEmbedding(self, query):
        try:
            response = self.openAiClient.embeddings.create(input=query, model=self.EMBEDDING_MODEL)
            embedding = response.data[0].embedding
            return embedding
        except Exception as e:
            print(f"Error in get_embedding: {e}")
            return None

    def getArticles(self, results):
        articlesData = list()
        db = self.mongoClient['All-PRO']
        collection = db['PRO-Noticias']
        for result in results:
            document = collection.find_one({'_id': ObjectId(result['id'])})
            articlesData.append(document)
        return articlesData
    
    def processArticles(self, articlesData, query):
        request = query
        for i,articleData in enumerate(articlesData):
            redaction_date = articleData.get('fecha_redaccion', '')
            active_subject = articleData.get('sujeto_activo', '')
            object_part = articleData.get('parte_objeto', '')
            main_topic = articleData.get('tema_principal', '')
            tone = articleData.get('tono', '')
            summary = articleData.get('resumen', '')
            keywords = articleData.get('palabras_clave', [])
            statements = articleData.get('declaraciones', [])

            request = f"{request}\n Noticia {i+1}: {redaction_date} {active_subject} {object_part} {main_topic} {tone} {summary} {' '.join(keywords)} {' '.join([dec['declaracion'] for dec in statements if 'declaracion' in dec])}"
        return request

if __name__ == '__main__':
    Program()  
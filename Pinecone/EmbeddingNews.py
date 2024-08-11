from pymongo import MongoClient
from openai import Client
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import PineconeException
import os
import warnings
from cryptography.utils import CryptographyDeprecationWarning

class Program():
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
        db = self.mongoClient['All-PRO']
        collection = db['PRO-Noticias']
        documents = list(collection.find())
        total_docs = len(documents)
        for i,document in enumerate(documents):
            print(f'Processing document {i + 1}/{total_docs}')
            if self.checkArticleInPinecone(document['_id']):
                print('The ID:', document['_id'], ' is already in Pinecone.')
            else:   
                self.embeddingNews(document)
    
    def embeddingNews(self, document):
        redaction_date = document.get('fecha_redaccion', '')
        active_subject = document.get('sujeto_activo', '')
        object_part = document.get('parte_objeto', '')
        main_topic = document.get('tema_principal', '')
        tone = document.get('tono', '')
        summary = document.get('resumen', '')
        keywords = document.get('palabras_clave', [])
        statements = document.get('declaraciones', [])

        processed_text = f"{redaction_date} {active_subject} {object_part} {main_topic} {tone} {summary} {' '.join(keywords)} {' '.join([dec['declaracion'] for dec in statements if 'declaracion' in dec])}"
        articleEmbedding = self.getEmbedding(document['_id'], processed_text)

        if articleEmbedding:
            self.pineconeInsert(document['_id'],articleEmbedding)
        else:
            print('Failed to generate embedding for the processed article', document['_id'])
            
    
    def getEmbedding(self, id, text):
        try:
            response = self.openAiClient.embeddings.create(input=text, model= self.EMBEDDING_MODEL)
            embedding = response.data[0].embedding
            return embedding
        except Exception as e:
            print(f"Error in article {id} getEmbedding: {e}")
            return None
        
    def pineconeInsert(self, id, embedding):
        try:
            self.index.upsert([(str(id), embedding)])
            print(f'Added one article ({id}) embedded to pinecone.')
        except PineconeException as e:
            print(f"Error: {str(e)}")


    def checkArticleInPinecone(self, id):
        response = self.index.fetch(ids=[str(id)])
        # In response, if vectors is null then returns False because there is no data wwith that ID
        return bool(response['vectors'])


if __name__ == '__main__':
    Program()   
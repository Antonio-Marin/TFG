from pymongo import MongoClient
from openai import Client
from pinecone.grpc import PineconeGRPC as Pinecone
import os
import warnings
from cryptography.utils import CryptographyDeprecationWarning

#TODO: hacer comprobaciones con el id de la noticia para ver si esta en pinecone primero antes de hacer el embedding
#TODO: si ocurre el error terminar la ejecuión y mostrar el id de la noticia con la que ocurrio el error
#TODO: de momento solo estoy probando con una noticia, una vez terminada la prueba hacerlo con el resto de noticas

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
        documents = collection.find_one()
        self.embeddingNews(documents)
        # for document in documents:
        #     self.embeddingNew(document)
    
    def embeddingNews(self, document):
        # print(document['_id'])
        redaction_date = document.get('fecha_redaccion', '')
        active_subject = document.get('sujeto_activo', '')
        object_part = document.get('parte_objeto', '')
        main_topic = document.get('tema_principal', '')
        tone = document.get('tono', '')
        summary = document.get('resumen', '')
        keywords = document.get('palabras_clave', [])
        statements = document.get('declaraciones', [])

        processed_text = f"{redaction_date} {active_subject} {object_part} {main_topic} {tone} {summary} {' '.join(keywords)} {' '.join([dec['declaracion'] for dec in statements if 'declaracion' in dec])}"
        print(processed_text)
        articleEmbedding = self.getEmbedding(document['_id'], processed_text)

        if articleEmbedding:
            self.pineconeInsert(document['_id'],articleEmbedding)
        else:
            print(f"Failed to generate embedding for the processed article")
            #TODO:¿sys.exit()?
            
    
    def getEmbedding(self, id, text):
        try:
            response = self.openAiClient.embeddings.create(input=text, model= self.EMBEDDING_MODEL)
            embedding = response.data[0].embedding
            return embedding
        except Exception as e:
            print(f"Error in article {id} get_embedding: {e}")
            return None
        
    def pineconeInsert(self, id, embedding):
        self.index.upsert([(str(id), embedding)])
        print('Added one article embedded to pinecone:')
        print(self.index.describe_index_stats(), '\t')


if __name__ == '__main__':
    Program()   
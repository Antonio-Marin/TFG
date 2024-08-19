from pymongo import MongoClient
from bson.objectid import ObjectId
from openai import Client
from pinecone.grpc import PineconeGRPC as Pinecone
import os
import gradio as gr
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

        #GRADIO
        interface = gr.Interface(
        fn=self.run, 
        inputs=gr.Textbox(label='Consulta', placeholder="Introduce tu consulta aquí..."), 
        outputs=gr.Textbox(label="Respuesta"), 
        title="Consultas COVID-19", 
        description="Introduce una consulta y se te proporcionara una respuesta en base a la información recopilada.",
        allow_flagging="manual",
        flagging_options=[("Marcar como errónea","Incorrecto")]
        )

        # EXECUTION
        interface.launch(share=True)

    def run(self, query):
        results = self.searchInPinecone(query)
        articlesData = self.getArticles(results)
        request = self.processArticles(articlesData, query)
        response = self.conclussion(request)
        return response

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
        request = f'Consulta: {query}'
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
    
    def conclussion(self, requestData):
        response = self.openAiClient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
            A continuación, te proporcionaré una consulta y una serie de noticias relacionadas. Por favor, analiza estas noticias y responde a la consulta anterior de manera concisa y clara, destacando los puntos más relevantes.
            """},
            {"role": "user", "content": requestData}
        ],
        temperature=0.5,    # Reduces randomness
        top_p=0.9           # Limit generation to the most likely tokens
        )

        response = response.choices[0].message.content
        return response

if __name__ == '__main__':
    Program()
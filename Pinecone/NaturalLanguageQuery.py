from pymongo import MongoClient
from bson.objectid import ObjectId
from openai import Client
from pinecone.grpc import PineconeGRPC as Pinecone
import os
import re
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
        outputs=[gr.Textbox(label="Respuesta"), gr.Markdown(label="Noticias")],
        title="Consultas COVID-19", 
        description="Introduce una consulta y se te proporcionara una respuesta en base a la información recopilada.",
        allow_flagging="never"
        )

        # EXECUTION
        interface.launch(share=True)

    def run(self, query):
        results = self.searchInPinecone(query)
        articlesData = self.getArticles(results)
        request = self.processArticles(articlesData, query)
        outputArticles = self.formatText(request)
        response = self.conclussion(request)
        return response, outputArticles

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
        request = f'Consulta: {query}\n'
        for i,articleData in enumerate(articlesData):
            request = f"""{request}\nNoticia {i+1}: \nFecha de Redacción: {articleData.get('fecha_redaccion', '')} \nSujeto Activo: {articleData.get('sujeto_activo', '')} \nParte Objeto: {articleData.get('parte_objeto', '')} \nTema Principal: {articleData.get('tema_principal', '')} \nTono: {articleData.get('tono', '')} \nResumen: {articleData.get('resumen', '')} \nPalabras Clave: {', '.join(articleData.get('palabras_clave', []))} \nDeclaraciones:"""
            if articleData.get('declaraciones', []):
                for declaration in articleData.get('declaraciones', []):
                    request += f"\n\t Entidad: {declaration.get('entidad', '')}, Declaración: {declaration.get('declaracion', '')}"
                request += f"\n"
            else:
                request += f" no hay declaraciones.\n"

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
    
    def formatText(self, text):
        text = re.sub(r"(Consulta:)", r" ## \1 ", text)
        text = re.sub(r"(Noticia \d+:)", r" ### \1 ", text)
        text = re.sub(r"(Fecha de Redacción:)", r" - **\1** ", text)
        text = re.sub(r"(Sujeto Activo:)", r" - **\1** ", text)
        text = re.sub(r"(Parte Objeto:)", r" - **\1** ", text)
        text = re.sub(r"(Tema Principal:)", r" - **\1** ", text)
        text = re.sub(r"(Tono:)", r" - **\1** ", text)
        text = re.sub(r"(Resumen:)", r" - **\1** ", text)
        text = re.sub(r"(Palabras Clave:)", r" - **\1** ", text)
        text = re.sub(r"(Declaraciones:)", r" - **\1** ", text)
        text = re.sub(r"(Entidad:)", r"\n   - **\1** ", text)
        text = re.sub(r"(Declaración:)", r" **\1** ", text)

        return text 

if __name__ == '__main__':
    Program()
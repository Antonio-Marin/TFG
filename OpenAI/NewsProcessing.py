import json
import openai
from openai import Client
import os
import tiktoken
import sys

class program:
    def __init__(self):
        #OpenAI API variables
        api_key = os.environ.get('OPENAI_API_KEY')
        self.client = Client(api_key=api_key)
        self.function_schema = {
            "name": "analizar_noticia",
            "description": "Analiza un artículo de noticias para extraer detalles específicos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fecha_redaccion": {
                        "type": "string",
                        "description": "La fecha en que se redactó el artículo de noticias."
                    },
                    "sujeto_activo": {
                        "type": "string",
                        "description": "La persona, entidad o grupo que es el foco principal de la noticia (por ejemplo, una entidad política, una organización internacional, un investigador)."
                    },
                    "parte_objeto": {
                        "type": "string",
                        "description": "La persona, entidad o grupo que es objeto de la noticia o críticas (por ejemplo, un gobierno, un partido político, una organización internacional)."
                    },
                    "tema_principal": {
                        "type": "string",
                        "description": "El tema principal del artículo de noticias."
                    },
                    "tono": {
                        "type": "string",
                        "description": "El tono del artículo de noticias (por ejemplo, neutral, positivo, negativo)."
                    },
                    "resumen": {
                        "type": "string",
                        "description": "Un breve resumen del artículo de noticias en una frase."
                    },
                    "palabras_clave": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Tres palabras clave que resumen el contenido del artículo de noticias."
                    },
                    "declaraciones": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "entidad": {"type": "string", "description": "El nombre de la entidad que hizo la declaración."},
                                "declaracion": {"type": "string", "description": "El contenido de la declaración."}
                            }
                        },
                        "description": "Lista de declaraciones hechas por entidades, con detalles sobre quién hizo la declaración y qué se dijo."
                    }
                },
                "required": ["fecha_redaccion", "sujeto_activo", "parte_objeto", "tema_principal", "tono", "resumen", "palabras_clave", "declaraciones"]
            }
        }

        # Global variables
        self.basePath = f'D:\Carrera\TFG\Pruebas de código\Mongo\DB'
        self.newscasts = ["ElMundo", "ElPais", "ElDiario", "LibertadDigital"]
        self.outputList = []
        self.totalJsons=0
        self.totalNews=0
        self.checkpoint_file = 'checkpoint.json'
        self.progress = self.load_progress()
        self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo-0125")
        self.max_tokens = 3830  # Maximum tokens i'm using
        # 3830 because the max is 4097 but i have already 266 in the functions

        # EXECUTION
        self.run()

    def load_progress(self):
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}

    def save_progress(self):
        with open(self.checkpoint_file, 'w', encoding='utf-8') as file:
            json.dump(self.progress, file, ensure_ascii=False, indent=4)

    def run(self):
        for newcast in self.newscasts:
            for filename in os.listdir(f'{self.basePath}\{newcast}'):
                if newcast in self.progress and filename in self.progress[newcast]:
                    continue  # Skip already processed files
                with open(f'{self.basePath}\{newcast}\{filename}', 'r', encoding='utf-8') as file:
                    print("================")
                    print(f'Opened: {newcast}\{filename}' )
                    newsData = json.load(file)
                    self.totalJsons+=1
                    for index, newData in enumerate(newsData, start=1):
                        print("----------------")
                        print(index,"/", len(newsData))
                        try:
                            title = newData['Título']
                        except:
                            title = newData['Titulo']
                        date = newData['Fecha']
                        body = newData['Cuerpo']
                        new = f"{title}\n{date}\n{body}"
                        # self.APIopenAI(new)
                        # Retry processing the news until it succeeds
                        while True:
                            if self.APIopenAI(new):
                                break  # Proceed to the next news if successful
                            # If the API call fails due to JSONDecodeError, retry processing
                            print("Retrying to process the news...")
                    self.writeJson(newcast, filename)
                    self.outputList.clear()
                    # Update progress
                    if newcast not in self.progress:
                        self.progress[newcast] = []
                    self.progress[newcast].append(filename)
                    self.save_progress()
        print('Number of jsons:',self.totalJsons)
        print('Total news:',self.totalNews)

    def APIopenAI(self, new):
        # Truncate the message if it exceeds the maximum token limit
        truncated_news = self.truncate_message(new)
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": """
                    Se te proporcionará una noticia sobre el coronavirus. Se espera que identifiques y extraigas la siguiente información:

                    1. Fecha de redacción: La fecha en que se redactó el artículo.
                    2. Sujeto activo: La persona, entidad o grupo que es el foco principal de la noticia (por ejemplo, una entidad política, una organización internacional, un investigador).
                    3. Parte objeto: La persona, entidad o grupo que es objeto de la noticia o críticas (por ejemplo, gobierno, un partido político, una organización internacional).
                    4. Tema principal: El tema principal del artículo.
                    5. Tono: El tono general del artículo (por ejemplo, neutral, positivo, negativo). El tono debe ser determinado en función del impacto emocional y la naturaleza de la información presentada.
                        - Negativo: Si la noticia trata sobre eventos preocupantes o desfavorables, como un aumento en el número de muertes o casos de una enfermedad, o críticas y ataques hacia partidos políticos o entidades políticas.
                        - Positivo: Si la noticia trata sobre eventos favorables, como avances médicos, reducción en casos de una enfermedad, o logros y reconocimientos hacia individuos o entidades.
                        - Neutral: Si la noticia presenta la información de manera objetiva, sin un claro impacto emocional positivo o negativo.
                    6. Resumen: Un breve resumen del artículo en una frase.
                    7. Palabras clave: Tres palabras clave que resuman el contenido del artículo.
                    8. Declaraciones: Identificar si la noticia contiene declaraciones de alguna persona o entidad relevante (por ejemplo, gobierno, partido político, experto). Si existen declaraciones, proporcionar detalles sobre quién hizo la declaración y el contenido de la misma.

                    El análisis debe ser objetivo y profesional, estructurado en secciones claras y organizadas para cada aspecto mencionado. Debes presentar los hallazgos de manera clara y coherente, sin añadir interpretaciones subjetivas, adoptando un enfoque neutral y preciso similar al de un analista de noticias o un investigador.
                    """},
                    {"role": "user", "content": truncated_news}
                ],
                functions=[self.function_schema],
                function_call={"name": "analizar_noticia"},
                temperature=0.5,    # Reduces randomness
                top_p=0.9           # Limit generation to the most likely tokens
            )

            function_response = response.choices[0].message.function_call
            try:
                arguments = json.loads(function_response.arguments)
                self.outputList.append(arguments)
            except json.JSONDecodeError as e:
                print("!!!!!!!!!!!!!!!!")
                print(f"JSON decode error: {e}")
                print(f"Function response: {function_response.arguments}")
                print("!!!!!!!!!!!!!!!!")
                return False
            # print('SALIDA DE LA NOTICIA', truncated_news, '\n\n', arguments)
            # print('-----------------------------------------------------')
            return True
        except openai.RateLimitError as e:
            print("!!!!!!!!!!!!!!!!")
            print(f"API call failed: {e}")
            print("!!!!!!!!!!!!!!!!")
            sys.exit()
        except openai.BadRequestError as e:
            print("!!!!!!!!!!!!!!!!")
            print(f"API call failed: {e}")
            print("!!!!!!!!!!!!!!!!")
            sys.exit()

    
    def truncate_message(self, message):
        tokens = self.tokenizer.encode(message)
        if len(tokens) > self.max_tokens:
            tokens = tokens[:self.max_tokens]
        return self.tokenizer.decode(tokens)


    def writeJson(self, folder, filename):
        pathJson = f'D:\Carrera\TFG\Pruebas de código\Pruebas OpenAI\ProcessedNews\{folder}\PRO-{filename}'
        with open(pathJson, 'w', encoding='utf-8') as jsonFile:
            json.dump(self.outputList, jsonFile, ensure_ascii=False, indent=4)

        print(f"News saved in JSON format, {pathJson}")
        print("-=-=-=-=-=-=-=-=")


if __name__ == '__main__':
    program()            
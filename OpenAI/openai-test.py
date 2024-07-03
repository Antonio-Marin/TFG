# import json
# from openai import Client
# import os

# def save_to_json(result):
#     with open('result.json', 'w', encoding='utf-8') as json_file:
#         json.dump(result, json_file, ensure_ascii=False, indent=4)

# with open('D:/Carrera/TFG/Pruebas de código/Pruebas OpenAI/test.json', 'r', encoding='utf-8') as file:
#     news_data = json.load(file)

# title = news_data['Título']
# date = news_data['Fecha']
# body = news_data['Cuerpo']

# new = f"{title}\n{date}\n{body}"

# api_key = os.environ.get('OPENAI_API_KEY')

# client = Client(api_key=api_key)

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "Se te proporcionará una noticia sobre el coronavirus, y se espera que identifiques la fecha de redacción, el sujeto activo de la información, el tema principal, el tono de la noticia, así como un breve resumen de una frase y tres palabras clave que resuman el contenido. El análisis debe ser objetivo y profesional, estructurado en secciones claras y organizadas para cada aspecto mencionado. Debes presentar los hallazgos de manera clara y coherente, sin añadir interpretaciones subjetivas, adoptando un enfoque neutral y preciso similar al de un analista de noticias o un investigador."},
#     {"role": "user", "content": new}
#   ]
# )

# #print(completion.choices[0].message.content)

# result_json = json.loads(completion.choices[0].message.content) 
# save_to_json(result_json)

import json
from openai import Client
import os

class program:
    def __init__(self):
        api_key = os.environ.get('OPENAI_API_KEY')
        self.client = Client(api_key=api_key)
        self.basePath = f'D:\Carrera\TFG\Pruebas de código\Pruebas OpenAI'
        self.filenames = ["NewsTest"]
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

        # self.newscasts = ["ElMundo", "ElPais", "ElDiario", "LibertadDigital"]
        self.outputList = []
        self.cont=0 #Number of jsons
        self.cont2=0 #Total news

        self.run()

    def run(self):
        for filename in self.filenames:
                with open(f'{self.basePath}\{filename}.json', 'r', encoding='utf-8') as file:
                    newsData = json.load(file)
                    self.cont+=1
                    for newData in newsData:
                        try:
                            title = newData['Título']
                        except:
                            title = newData['Titulo']
                        date = newData['Fecha']
                        body = newData['Cuerpo']
                        new = f"{title}\n{date}\n{body}"
                        self.cont2+=1
                        self.APIopenAI(new)
                    self.writeJson(filename)
                    self.outputList.clear()
        print('Number of jsons:',self.cont)
        print('Total news:',self.cont2)

    def APIopenAI(self, new):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
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
                {"role": "user", "content": new}
            ],
            functions=[self.function_schema],
            function_call={"name": "analizar_noticia"},
            temperature=0.5,    # Reduces randomness
            top_p=0.9           # Limit generation to the most likely tokens
        )

        function_response = response.choices[0].message.function_call

        arguments = json.loads(function_response.arguments)
        self.outputList.append(arguments)
        print('SALIDA DE LA NOTICIA', new, '\n\n', arguments)
        print('-----------------------------------------------------')

    def writeJson(self, filename):
        pathJson = f'D:\Carrera\TFG\Pruebas de código\Pruebas OpenAI\PRO-{filename}.json'
        with open(pathJson, 'w', encoding='utf-8') as jsonFile:
            json.dump(self.outputList, jsonFile, ensure_ascii=False, indent=4)

        print(f"News saved in JSON format, {pathJson}")

if __name__ == '__main__':
    program()
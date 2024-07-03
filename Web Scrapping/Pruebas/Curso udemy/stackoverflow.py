import requests
from bs4 import BeautifulSoup

encabezado = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

url = "https://stackoverflow.com/questions"

respuesta = requests.get(url, headers=encabezado)

soup = BeautifulSoup(respuesta.text, features="html.parser")

contenedor_preguntas = soup.find(id="questions")
lista_preguntas = contenedor_preguntas.find_all('div', class_="s-post-summary")

for pregunta in lista_preguntas:
    txt_pregunta = pregunta.find('h3').text
    desc_pregunta = pregunta.find(class_="s-post-summary--content-excerpt").text
    print("PREGUNTA: ",txt_pregunta)
    print("DESCRIPCIÓN: ",desc_pregunta)
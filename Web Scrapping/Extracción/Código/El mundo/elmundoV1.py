from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv

#VARIABLES GLOBALES
anio= ["2020","2021","2022"]
fechas = [
    "01/01", "01/02", "01/03", "01/04", "01/05", "01/06", "01/07", "01/08", "01/09", "01/10", "01/11", "01/12", "01/13", "01/14", "01/15", "01/16", "01/17", "01/18", "01/19", "01/20", "01/21", "01/22", "01/23", "01/24", "01/25", "01/26", "01/27", "01/28", "01/29", "01/30", "01/31",
    "02/01", "02/02", "02/03", "02/04", "02/05", "02/06", "02/07", "02/08", "02/09", "02/10", "02/11", "02/12", "02/13", "02/14", "02/15", "02/16", "02/17", "02/18", "02/19", "02/20", "02/21", "02/22", "02/23", "02/24", "02/25", "02/26", "02/27", "02/28",
    "03/01", "03/02", "03/03", "03/04", "03/05", "03/06", "03/07", "03/08", "03/09", "03/10", "03/11", "03/12", "03/13", "03/14", "03/15", "03/16", "03/17", "03/18", "03/19", "03/20", "03/21", "03/22", "03/23", "03/24", "03/25", "03/26", "03/27", "03/28", "03/29", "03/30", "03/31",
    "04/01", "04/02", "04/03", "04/04", "04/05", "04/06", "04/07", "04/08", "04/09", "04/10", "04/11", "04/12", "04/13", "04/14", "04/15", "04/16", "04/17", "04/18", "04/19", "04/20", "04/21", "04/22", "04/23", "04/24", "04/25", "04/26", "04/27", "04/28", "04/29", "04/30",
    "05/01", "05/02", "05/03", "05/04", "05/05", "05/06", "05/07", "05/08", "05/09", "05/10", "05/11", "05/12", "05/13", "05/14", "05/15", "05/16", "05/17", "05/18", "05/19", "05/20", "05/21", "05/22", "05/23", "05/24", "05/25", "05/26", "05/27", "05/28", "05/29", "05/30", "05/31",
    "06/01", "06/02", "06/03", "06/04", "06/05", "06/06", "06/07", "06/08", "06/09", "06/10", "06/11", "06/12", "06/13", "06/14", "06/15", "06/16", "06/17", "06/18", "06/19", "06/20", "06/21", "06/22", "06/23", "06/24", "06/25", "06/26", "06/27", "06/28", "06/29", "06/30",
    "07/01", "07/02", "07/03", "07/04", "07/05", "07/06", "07/07", "07/08", "07/09", "07/10", "07/11", "07/12", "07/13", "07/14", "07/15", "07/16", "07/17", "07/18", "07/19", "07/20", "07/21", "07/22", "07/23", "07/24", "07/25", "07/26", "07/27", "07/28", "07/29", "07/30", "07/31",
    "08/01", "08/02", "08/03", "08/04", "08/05", "08/06", "08/07", "08/08", "08/09", "08/10", "08/11", "08/12", "08/13", "08/14", "08/15", "08/16", "08/17", "08/18", "08/19", "08/20", "08/21", "08/22", "08/23", "08/24", "08/25", "08/26", "08/27", "08/28", "08/29", "08/30", "08/31",
    "09/01", "09/02", "09/03", "09/04", "09/05", "09/06", "09/07", "09/08", "09/09", "09/10", "09/11", "09/12", "09/13", "09/14", "09/15", "09/16", "09/17", "09/18", "09/19", "09/20", "09/21", "09/22", "09/23", "09/24", "09/25", "09/26", "09/27", "09/28", "09/29", "09/30",
    "10/01", "10/02", "10/03", "10/04", "10/05", "10/06", "10/07", "10/08", "10/09", "10/10", "10/11", "10/12", "10/13", "10/14", "10/15", "10/16", "10/17", "10/18", "10/19", "10/20", "10/21", "10/22", "10/23", "10/24", "10/25", "10/26", "10/27", "10/28", "10/29", "10/30", "10/31",
    "11/01", "11/02", "11/03", "11/04", "11/05", "11/06", "11/07", "11/08", "11/09", "11/10", "11/11", "11/12", "11/13", "11/14", "11/15", "11/16", "11/17", "11/18", "11/19", "11/20", "11/21", "11/22", "11/23", "11/24", "11/25", "11/26", "11/27", "11/28", "11/29", "11/30",
    "12/01", "12/02", "12/03", "12/04", "12/05", "12/06", "12/07", "12/08", "12/09", "12/10", "12/11", "12/12", "12/13", "12/14", "12/15", "12/16", "12/17", "12/18", "12/19", "12/20", "12/21", "12/22", "12/23", "12/24", "12/25", "12/26", "12/27", "12/28", "12/29", "12/30", "12/31"
]
fb = "02/29" #Como 2020 es bisiesto agregamos el 29-02 en una variable
portada = ["m","t","n"]
URL_BASE= "https://www.elmundo.es/elmundo/hemeroteca/" #Si no se indica el año te redirecciona a 2024
filtros = ["coronavirus", "covid-19", "pandemia", "vacuna", "contagio", "cuarentena", "síntomas","confinamiento", "distanciamiento", "cierre",
         "contagios","contagio", "virus", "wuhan", "epidemia", "brote","brotes", "aislamiento", "sars-cov-2", "transmisión", "variante", "variantes",
         "cepa", "mascarilla", "uci", "teletrabajo"]

#CACHE PARA EVITAR ACCEDER MAS DE UNA VEZ A LA MISMA NOTICIA
cache_titulos = []

#RESULTADOS
result_temas = []
result_titulos = []
result_cuerpos = []
enlaces = []

class program:
    def __init__(self):
        #DRIVER
        #Preparacion del driver
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36") #Buscar el user-agent

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opts
        )

        for a in anio:
            for f in fechas:
                for p in portada:
                    url = f"{URL_BASE}{a}/{f}/{p}"
                    program.news(driver, url)

                    if a=="2020" and f == "02/28":
                        program.news(driver, url)
        
        # print("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")
        # print("RESULTADO FINAL:")
        # print("TEMA: ", result_temas)
        # print("TITULO: ", result_titulos)
        # print("CUERPO NOTICIA: ", result_cuerpos)
        # print("ENLACE: ", enlaces)
        # print("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")

        # PARA EL CSV
        datos=zip(result_temas,result_titulos, result_cuerpos, enlaces)
        program.writeCsv(datos)

        driver.quit()

        """
        #MAS ADELANTE
        for a in anio:
            for f in fechas:
                for p in portada:
                    url = f"{URL_BASE}{a}/{f}/{p}"
                    
                    print(url)
                    #driver.get(url)
                    #procedimiento de extracción de datos...
                    if a=="2020" and f == "02/28":
                        url = f"{URL_BASE}{a}/{fb}/{p}"
                        print(url)
                        #driver.get(url)
                        #procedimiento de extracción de datos...
        """
    def news(driver, url):
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, features='html.parser')
        noticias = soup.find_all('header', class_='ue-c-cover-content__headline-group')
        program.newArticle(noticias, driver)

    def newArticle(noticias, driver):
        for noticia in noticias:
            try:
                #print("NOTICIA: ",noticia)
                titulo = noticia.find('a', class_='ue-c-cover-content__link').text
                #print("TITULO: ", titulo)
                if titulo not in cache_titulos:
                    tema = noticia.find('span', class_='ue-c-cover-content__kicker').text
                    #print("TEMA: ", tema)
                    tema_pro = tema.lower().replace(" ", "").replace(".", "")
                    titulo_pro = titulo.lower().replace(".", "")

                    titulo_pal = titulo_pro.split()

                    if tema_pro  in filtros or program.themeInTitle(titulo_pal): # "FILTRO"
                        enlace = noticia.find('a', class_='ue-c-cover-content__link')['href']
                        #print("ENLACE", enlace)
                        result_temas.append(tema)
                        result_titulos.append(titulo)
                        enlaces.append(enlace)

                        driver.get(enlace)
                        html_noticia = driver.page_source
                        soup_noticia = BeautifulSoup(html_noticia, features='html.parser')
                        result_cuerpos.append(program.inArticle(soup_noticia))

                    cache_titulos.append(titulo)
                # print("==========================================================")

            except AttributeError:
                pass
                # print("OPINIÓN")
                # print("==========================================================")
            
    def inArticle(soup):
        subtitulo_noticia = soup.find('p', class_='ue-c-article__standfirst').text
        cuerpo_noticia = soup.find_all('div', class_='ue-l-article__body ue-c-article__body')
        aux = ""
        for element in cuerpo_noticia:
            parrafos = element.find_all('p')
            for parrafo in parrafos:
                if parrafo.text != "Conforme a los criterios deThe Trust Project":
                    aux+= parrafo.text
        return subtitulo_noticia+aux
    
    def themeInTitle(titulo_pal):
        for titulo in titulo_pal:
            if len(titulo)>4 and titulo in filtros :
                return True
        
        return False
    def writeCsv(datos):
        archivo_csv = 'datos.csv'

        with open(archivo_csv, 'w', newline='', encoding='utf-8') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
                
            escritor_csv.writerow(['Tema', 'Título', 'Cuerpo','Enlace'])
               
            escritor_csv.writerows(datos)

        print("Archivo CSV ",archivo_csv," creado exitosamente.")
        #print("__________________________________________________________")

if __name__ == '__main__':
    program()

"""
GUIA DE COMO FUNCIONA LAS PAGINAS
Paginas donde hay un calendario con las noticias que me interesa sacar:
https://www.elmundo.es/elmundo/hemeroteca/2020/
https://www.elmundo.es/elmundo/hemeroteca/2021/
https://www.elmundo.es/elmundo/hemeroteca/2022/

Enlaces donde esta la información:
https://www.elmundo.es/elmundo/hemeroteca/2020/02/01/m/index.html
https://www.elmundo.es/elmundo/hemeroteca/2020/02/01/t/index.html
https://www.elmundo.es/elmundo/hemeroteca/2020/02/01/n/index.html

DONDE ME INTERESA RECOGER LOS DATOS
Clase donde esta la noticia (<header class = "ue-c-cover-content__headline-group">) 
con su tema (<span class= "ue-c-cover-content__kicker">) 
y dentro un enlace (<a class= "ue-c-cover-content__link">) 
con el titular (<h2 class = "ue-c-cover-content__headline">)
Dentro de los articulos que te coja el h1 y todas las p
"""
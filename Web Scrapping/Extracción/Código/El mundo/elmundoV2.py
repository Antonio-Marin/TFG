from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import calendar

#VARIABLES GLOBALES
anios= ["2020","2021","2022"]
meses = ['01','02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
portada = ["m","t","n"]
URL_BASE= "https://www.elmundo.es/elmundo/hemeroteca/"
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
        #Preparacion del driver
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36") #Buscar el user-agent

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opts
        )

        for a in anios:
            for m in meses:
                ultimo_dia = calendar.monthrange(int(a), int(m))[1]
        
                # Ajustar el rango para años bisiestos
                if calendar.isleap(int(a)) and m == "02":
                    dias_del_mes = [str(d).zfill(2) for d in range(1, ultimo_dia + 1)]
                else:
                    dias_del_mes = [str(d).zfill(2) for d in range(1, ultimo_dia)]
                for d in dias_del_mes:
                    for p in portada:
                        url = f"{URL_BASE}{a}/{m}/{d}/{p}"
                        program.news(driver, url)

                #CSV
                datos=zip(result_temas,result_titulos, result_cuerpos, enlaces)
                fecha= f'_{a}-{m}'
                program.writeCsv(datos, fecha)

        driver.quit()

    # FUNCIONES
    def news(driver, url):
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, features='html.parser')
        noticias = soup.find_all('header', class_='ue-c-cover-content__headline-group')
        program.newArticle(noticias, driver)

    def newArticle(noticias, driver):
        for noticia in noticias:
            try:
                titulo = noticia.find('a', class_='ue-c-cover-content__link').text
                if titulo not in cache_titulos:
                    tema = noticia.find('span', class_='ue-c-cover-content__kicker').text
                    tema_pro = tema.lower().replace(" ", "").replace(".", "")
                    titulo_pro = titulo.lower().replace(".", "")

                    titulo_pal = titulo_pro.split()

                    if tema_pro  in filtros or program.themeInTitle(titulo_pal): # "FILTRO"
                        enlace = noticia.find('a', class_='ue-c-cover-content__link')['href']
                        result_temas.append(tema)
                        result_titulos.append(titulo)
                        enlaces.append(enlace)

                        driver.get(enlace)
                        html_noticia = driver.page_source
                        soup_noticia = BeautifulSoup(html_noticia, features='html.parser')
                        result_cuerpos.append(program.inArticle(soup_noticia))

                    cache_titulos.append(titulo)

            except AttributeError:
                pass
            
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
    def writeCsv(datos, fecha):
        archivo_csv = f'datos{fecha}.csv'

        with open(archivo_csv, 'w', newline='', encoding='utf-8') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
                
            escritor_csv.writerow(['Tema', 'Título', 'Cuerpo','Enlace'])
               
            escritor_csv.writerows(datos)

        print("Archivo CSV ",archivo_csv," creado exitosamente.")

    def cleanGlobalVars():
        result_temas.clear()
        result_titulos.clear()
        result_cuerpos.clear()
        enlaces.clear()
        cache_titulos.clear()


if __name__ == '__main__':
    program()

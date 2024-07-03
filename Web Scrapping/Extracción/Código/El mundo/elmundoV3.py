from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import calendar
import os

class program:
    def __init__(self):
        #VARIABLES GLOBALES
        self.anios= ["2020","2021","2022"]
        self.meses = ['01','02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.portada = ["m","t","n"]
        self.URL_BASE= "https://www.elmundo.es/elmundo/hemeroteca/"
        self.filtros = ["coronavirus", "covid-19", "pandemia", "vacuna", "contagio", "cuarentena", "síntomas","confinamiento", "distanciamiento", "cierre",
                "contagios","contagio", "virus", "wuhan", "epidemia", "brote","brotes", "aislamiento", "sars-cov-2", "transmisión", "variante", "variantes",
                "cepa", "mascarilla", "uci", "teletrabajo"]

        #CACHE PARA EVITAR ACCEDER MAS DE UNA VEZ A LA MISMA NOTICIA
        self.cache_titulos = []

        #RESULTADOS
        self.lista_noticias = []

        #EJECUCION
        self.run()

    def run(self):

        # Cargar información del checkpoint si existe
        checkpoint_info = self.load_checkpoint()
        start_year = checkpoint_info.get("year", "2020")
        start_month = checkpoint_info.get("month", "01")

        #Preparacion del driver
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36") #Buscar el user-agent

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opts
        )

        for a in self.anios[self.anios.index(start_year):]:
            for m in self.meses[self.meses.index(start_month):]:
                ultimo_dia = calendar.monthrange(int(a), int(m))[1]
        
                # Ajustar el rango para años bisiestos
                if calendar.isleap(int(a)) and m == "02":
                    dias_del_mes = [str(d).zfill(2) for d in range(1, ultimo_dia + 1)]
                else:
                    dias_del_mes = [str(d).zfill(2) for d in range(1, ultimo_dia)]

                for d in dias_del_mes:
                    for p in self.portada:
                        url = f"{self.URL_BASE}{a}/{m}/{d}/{p}"
                        program.news(self, driver, url)

                #JSON
                fecha= f'_{a}-{m}'
                program.writeJson(self,fecha)
                self.cache_titulos.clear()
                self.lista_noticias.clear()

                # Actualizar checkpoint
                self.update_checkpoint(a, m)


        driver.quit()

    # FUNCIONES
    def news(self, driver, url):
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, features='html.parser')
        noticias = soup.find_all('header', class_='ue-c-cover-content__headline-group')
        program.newArticle(self, noticias, driver)

    def newArticle(self, noticias, driver):
        for noticia in noticias:
            try:
                titulo = noticia.find('a', class_='ue-c-cover-content__link').text
                if titulo not in self.cache_titulos:
                    tema = noticia.find('span', class_='ue-c-cover-content__kicker').text
                    tema_pro = tema.lower().replace(" ", "").replace(".", "")
                    titulo_pro = titulo.lower().replace(".", "")

                    titulo_pal = titulo_pro.split()

                    if tema_pro  in self.filtros or program.themeInTitle(self, titulo_pal): # "FILTRO"
                        enlace = noticia.find('a', class_='ue-c-cover-content__link')['href']
                        diccionario_noticia = dict()

                        diccionario_noticia['Tema'] = tema
                        diccionario_noticia['Título'] = titulo

                        driver.get(enlace)
                        html_noticia = driver.page_source
                        soup_noticia = BeautifulSoup(html_noticia, features='html.parser')
                        diccionario_noticia['Cuerpo'] = program.inArticle(soup_noticia)
                        diccionario_noticia['Enlace'] = enlace
                        self.lista_noticias.append(diccionario_noticia)

                    self.cache_titulos.append(titulo)

            except AttributeError:
                #Artículos que no son noticias
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
        return f'{subtitulo_noticia}. {aux}'
    
    def themeInTitle(self ,titulo_pal):
        for titulo in titulo_pal:
            if len(titulo)>4 and titulo in self.filtros :
                return True
        
        return False
    def writeJson(self, fecha):
        ruta_json = f'D:\Carrera\TFG\Pruebas de código\Extraccion\jsons\El mundo\datos{fecha}.json'
        with open(ruta_json, 'w', encoding='utf-8') as archivo_json:
            json.dump(self.lista_noticias, archivo_json, ensure_ascii=False, indent=4)

        print(f"Noticias guardada en formato JSON, {ruta_json}")

    def load_checkpoint(self):
        checkpoint_file = 'D:\Carrera\TFG\Pruebas de código\Extraccion\checkpoint\checkpoint_mundo.json'
        if os.path.exists(checkpoint_file):
            with open(checkpoint_file, 'r') as f:
                return json.load(f)
        return {}

    def update_checkpoint(self, current_year, current_month):
        checkpoint_info = {"year": current_year, "month": current_month}
        checkpoint_file = 'D:\Carrera\TFG\Pruebas de código\Extraccion\checkpoint\checkpoint_mundo.json'
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_info, f)

if __name__ == '__main__':
    program()

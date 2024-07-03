from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36") #Buscar el user-agent

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)

url2 = "https://static.elpais.com/hemeroteca/elpais/2022/12/01/m/portada.html"
driver.get(url2)
html = driver.page_source
soup = BeautifulSoup(html, features='html.parser')
titulos = soup.find_all('h2', class_='c_t')
for titulo in titulos:
    print(titulo.text)
    print(titulo.a['href'])


# driver.get('https://static.elpais.com/hemeroteca/elpais/2020/05/11/n/portada.html')
# html = driver.page_source
# soup = BeautifulSoup(html, features='html.parser')
# titulos = soup.find_all('h2', class_='headline')
# for titulo in titulos:
#     print(titulo.text)
#     print(titulo.find('a')['href'])

# driver.get('https://elpais.com/economia/2020-05-11/las-aerolineas-rechazan-bajar-la-ocupacion-de-los-vuelos-y-avisan-de-que-le-puede-llevar-a-la-quiebra.html')
# html_noticia = driver.page_source
# soup_noticia = BeautifulSoup(html_noticia, features='html.parser')
# subtitulo =  soup_noticia.find('h2', class_='a_st').text
# aux = ""
# div_cuerpo = soup_noticia.find('div', class_='a_c clearfix')
# parrafos = div_cuerpo.find_all('p')
# for parrafo in parrafos:
#     if parrafo.get_text(strip=True) != 'O suscríbete para leer sin límites':
#         aux+= parrafo.text
# print(f'{subtitulo}. {aux}')

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# import json
# import calendar
# import os
# import sys

# class program:
#     def __init__(self):
#          #VARIABLES GLOBALES
#         self.anios= ["2020","2021","2022"]
#         self.meses = ['01','02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#         self.portada = ["m","t","n"]
#         self.url_base= "https://elpais.com/hemeroteca/elpais/"
#         self.url_base2= "https://static.elpais.com/hemeroteca/elpais/"
#         self.filtros = ["coronavirus", "covid-19", "pandemia", "vacuna", "contagio", "cuarentena", "síntomas","confinamiento", "distanciamiento", "cierre",
#                 "contagios","contagio", "virus", "wuhan", "epidemia", "brote","brotes", "aislamiento", "sars-cov-2", "transmisión", "variante", "variantes",
#                 "cepa", "mascarilla", "uci", "teletrabajo"]
#         self.is_static= False

#         #CACHE PARA EVITAR ACCEDER MAS DE UNA VEZ A LA MISMA NOTICIA
#         self.cache_titulos = []

#         #RESULTADOS
#         self.lista_noticias = []

#         #EJECUCION
#         self.run()

#     def run(self):
#         # Cargar información del checkpoint si existe
#         checkpoint_info = self.load_checkpoint()
#         start_year = checkpoint_info.get("year", "2020")
#         start_month = checkpoint_info.get("month", "01")

#         #Preparacion del driver
#         opts = Options()
#         opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36") #Buscar el user-agent

#         driver = webdriver.Chrome(
#             service=Service(ChromeDriverManager().install()),
#             options=opts
#         )

#         for a in self.anios[self.anios.index(start_year):]:
#             for m in self.meses[self.meses.index(start_month):]:
#                 ultimo_dia = calendar.monthrange(int(a), int(m))[1]
        
#                 # Ajustar el rango para años bisiestos
#                 if calendar.isleap(int(a)) and m == "02":
#                     dias_del_mes = [str(d).zfill(2) for d in range(1, ultimo_dia + 1)]
#                 else:
#                     dias_del_mes = [str(d).zfill(2) for d in range(1, ultimo_dia)]

#                 for d in dias_del_mes:
#                     for p in self.portada:
#                         if self.is_static:
#                             url2 = f"{self.url_base2}{a}/{m}/{d}/{p}/portada.html"
#                             program.news2(self, driver, url2)
#                         else:
#                             url = f"{self.url_base}{a}/{m}/{d}/{p}/portada.html"
#                             if url == "https://elpais.com/hemeroteca/elpais/2020/05/11/n/portada.html":
#                                 self.is_static= True
#                 #JSON
#                 fecha= f'_{a}-{m}'
#                 program.writeJson(self,fecha)
#                 self.cache_titulos.clear()
#                 self.lista_noticias.clear()
                
#                 # Actualizar checkpoint
#                 self.update_checkpoint(a, m)

#         driver.quit()

#     # FUNCIONES
#     # def news(self, driver, url):
#     #     driver.get(url)
#     #     html = driver.page_source
#     #     soup = BeautifulSoup(html, features='html.parser')
#     #     titulos = soup.find_all('h2', class_='articulo-titulo')
#     #     program.newArticle(self, titulos, driver)

#     def news2(self, driver, url2):
#         driver.get(url2)
#         html = driver.page_source
#         soup = BeautifulSoup(html, features='html.parser')
#         titulos = soup.find_all('h2', class_='headline')
#         program.newArticle(self, titulos, driver)
        
#     def newArticle(self, noticias, driver):
#         for noticia in noticias:
#             titulo = noticia.text
#             if titulo not in self.cache_titulos:
#                 titulo_pro = titulo.lower().replace(".", "")
#                 titulo_pal = titulo_pro.split()

#                 if program.themeInTitle(self, titulo_pal): # "FILTRO"
#                     diccionario_noticia = dict()
#                     diccionario_noticia['Título'] = titulo
#                     print("TITULO NOTICIA: ", titulo)
#                     enlace = noticia.find('a')['href']
#                     print("ENLACE NOTICIA: ", enlace)

#                     try:
#                         driver.get(enlace)
#                     except:
#                         enlace = f'https://elpais.com{enlace}'
#                         driver.get(enlace)
                        
#                     html_noticia = driver.page_source
#                     soup_noticia = BeautifulSoup(html_noticia, features='html.parser')
                    
#                     diccionario_noticia['Cuerpo'] = program.inArticle(soup_noticia)
#                     diccionario_noticia['Enlace'] = enlace

#                     self.lista_noticias.append(diccionario_noticia)

#                 self.cache_titulos.append(titulo)

#     def inArticle(soup):
#         try:
#             subtitulo =  soup.find('h2', class_='a_st').text
#             aux = ""
#             div_cuerpo = soup.find('div', class_='a_c clearfix')
#             parrafos = div_cuerpo.find_all('p')
#             for parrafo in parrafos:
#                 if parrafo.get_text(strip=True) != 'O suscríbete para leer sin límites':
#                     aux+= parrafo.text
#             return f'{subtitulo}. {aux}'
#         except AttributeError:
#             #Artículos con formato distinto
#             pass
    
#     def themeInTitle(self ,titulo_pal):
#         for titulo in titulo_pal:
#             if len(titulo)>4 and titulo in self.filtros :
#                 return True
#         return False
    
#     def writeJson(self, fecha):
#         ruta_json = f'D:\Carrera\TFG\Pruebas de código\Extraccion\jsons\El pais\datos{fecha}.json'
#         with open(ruta_json, 'w', encoding='utf-8') as archivo_json:
#             json.dump(self.lista_noticias, archivo_json, ensure_ascii=False, indent=4)

#         print(f"Noticias guardada en formato JSON, {ruta_json}")

#     def load_checkpoint(self):
#         checkpoint_file = 'D:\Carrera\TFG\Pruebas de código\Extraccion\checkpoint\checkpoint_pais.json'
#         if os.path.exists(checkpoint_file):
#             with open(checkpoint_file, 'r') as f:
#                 return json.load(f)
#         return {}

#     def update_checkpoint(self, current_year, current_month):
#         checkpoint_info = {"year": current_year, "month": current_month}
#         checkpoint_file = 'D:\Carrera\TFG\Pruebas de código\Extraccion\checkpoint\checkpoint_pais.json'
#         with open(checkpoint_file, 'w') as f:
#             json.dump(checkpoint_info, f)

# if __name__ == '__main__':
#     program()
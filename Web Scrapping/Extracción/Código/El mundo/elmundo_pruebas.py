import sys

for i in range(0,3):
    if i != 1:
        print("a")
    else:
        sys.exit()
    print(i)

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# import json
# import calendar
# import time

# #VARIABLES GLOBALES
# anios= ["2020"]
# meses = ['02']
# portada = ["m"]
# URL_BASE= "https://www.elmundo.es/elmundo/hemeroteca/"
# filtros = ["coronavirus", "covid-19", "pandemia", "vacuna", "contagio", "cuarentena", "síntomas","confinamiento", "distanciamiento", "cierre",
#          "contagios","contagio", "virus", "wuhan", "epidemia", "brote","brotes", "aislamiento", "sars-cov-2", "transmisión", "variante", "variantes",
#          "cepa", "mascarilla", "uci", "teletrabajo"]

# #CACHE PARA EVITAR ACCEDER MAS DE UNA VEZ A LA MISMA NOTICIA
# cache_titulos = []
# diccionario_noticia = {}

# #RESULTADOS
# lista_noticias = []

# class program:
#     def __init__(self):
        
#         #Preparacion del driver
#         opts = Options()
#         opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36") #Buscar el user-agent

#         driver = webdriver.Chrome(
#             service=Service(ChromeDriverManager().install()),
#             options=opts
#         )

#         for a in anios:
#             for m in meses:
#                 #lista_noticias.clear()
#                 #ultimo_dia = calendar.monthrange(int(a), int(m))[1]
        
#                 # Ajustar el rango para años bisiestos
#                 # if calendar.isleap(int(a)) and m == "02":
#                 #     dias_del_mes = [str(d).zfill(2) for d in range(1, ultimo_dia + 1)]
#                 # else:
#                 #     dias_del_mes = [str(d).zfill(2) for d in range(1, ultimo_dia)]
#                 # for d in dias_del_mes:
#                 dias_prueba = ['01','02']
#                 for d in dias_prueba:
#                     for p in portada:
#                         url = f"{URL_BASE}{a}/{m}/{d}/{p}"
#                         program.news(driver, url)

#                 #JSON
#                 fecha= f'_{a}-{m}'
#                 program.writeJson(lista_noticias,fecha)
#                 #lista_noticias.clear()


#         driver.quit()

#     # FUNCIONES
#     def news(driver, url):
#         driver.get(url)
#         #TODO: aceptar cookies
#         html = driver.page_source
#         soup = BeautifulSoup(html, features='html.parser')
#         noticias = soup.find_all('header', class_='ue-c-cover-content__headline-group')
#         program.newArticle(noticias, driver)

#     def newArticle(noticias, driver):
#         for noticia in noticias:
#             try:
#                 titulo = noticia.find('a', class_='ue-c-cover-content__link').text
#                 if titulo not in cache_titulos:
#                     tema = noticia.find('span', class_='ue-c-cover-content__kicker').text
#                     tema_pro = tema.lower().replace(" ", "").replace(".", "")
#                     titulo_pro = titulo.lower().replace(".", "")

#                     titulo_pal = titulo_pro.split()

#                     if tema_pro  in filtros or program.themeInTitle(titulo_pal): # "FILTRO"
#                         enlace = noticia.find('a', class_='ue-c-cover-content__link')['href']
#                         diccionario_noticia['Tema'] = tema
#                         diccionario_noticia['Título'] = titulo

#                         driver.get(enlace)
#                         html_noticia = driver.page_source
#                         soup_noticia = BeautifulSoup(html_noticia, features='html.parser')
#                         diccionario_noticia['Cuerpo'] = program.inArticle(soup_noticia)
#                         diccionario_noticia['Enlace'] = enlace
#                         print('==============================================================================')
#                         print('DICCIONARIO NOTICIA: ', diccionario_noticia)
#                         print('------------------------------------------------------------------------------')
#                         lista_noticias.append(diccionario_noticia)
#                         print('LISTA NOTICIA: ', lista_noticias)
#                         diccionario_noticia.clear()
#                         print('------------------------------------------------------------------------------')
#                         print('DICCIONARIO NOTICIA VACIO: ', diccionario_noticia)
#                         print('==============================================================================')

#                     cache_titulos.append(titulo)

#             except AttributeError:
#                 pass
            
#     def inArticle(soup):
#         subtitulo_noticia = soup.find('p', class_='ue-c-article__standfirst').text
#         cuerpo_noticia = soup.find_all('div', class_='ue-l-article__body ue-c-article__body')
#         aux = ""
#         for element in cuerpo_noticia:
#             parrafos = element.find_all('p')
#             for parrafo in parrafos:
#                 if parrafo.text != "Conforme a los criterios deThe Trust Project":
#                     aux+= parrafo.text
#         return subtitulo_noticia+aux
    
#     def themeInTitle(titulo_pal):
#         for titulo in titulo_pal:
#             if len(titulo)>4 and titulo in filtros :
#                 return True
        
#         return False
#     def writeJson(lista, fecha):
#         ruta_json = f'D:\Carrera\TFG\Pruebas de código\Extraccion\jsons\datos{fecha}.json'
#         print('LISTA NOTICIAS AL ESCRIBIR EL JSON: ', lista)
#         with open(ruta_json, 'w', encoding='utf-8') as archivo_json:
#             json.dump(lista, archivo_json, ensure_ascii=False, indent=4)

#         print(f"Noticias guardada en formato JSON, {ruta_json}")

# if __name__ == '__main__':
#     program()


#PRUEBA PARA SACAR EL CONTENIDO DE LA NOTICIA
# driver.get('https://www.elmundo.es/salud/2020/02/01/5e354c72fdddff45498b4618.html')

# html_noticia = driver.page_source
# soup_noticia = BeautifulSoup(html_noticia, features='html.parser')
# subtitulo_noticia = soup_noticia.find('p', class_='ue-c-article__standfirst').text
# cuerpo_noticia = soup_noticia.find_all('div', class_='ue-l-article__body ue-c-article__body')
# aux = ""
# for element in cuerpo_noticia:
#     elements2 = element.find_all('p')
#     for i in elements2:
#         if i.text != "Conforme a los criterios deThe Trust Project":
#             aux+= i.text
# print("SUBTITULO:", subtitulo_noticia)
# print("=================================================")
# print("CUERPO: ",aux)

#PRUEBA DE LOS FILTROS
# driver.get('https://www.elmundo.es/elmundo/hemeroteca/2020/02/01/m')
# html = driver.page_source
# soup = BeautifulSoup(html, features='html.parser')
# noticias = soup.find_all('header', class_='ue-c-cover-content__headline-group')

# for noticia in noticias:
#     try:
#         tema = noticia.find('span', class_='ue-c-cover-content__kicker').get_text(strip=True)
#         print("TEMA: ", tema)
#         titulo = noticia.find('a', class_='ue-c-cover-content__link').text
#         print("TITULO: ", titulo)

#         tema_pro = tema.lower().replace(" ", "").replace(".", "")
#         print('TEMA PROCESADO: ',tema_pro)

#         titulo_pro = titulo.lower().replace(".", "")
#         print('TITULO PROCESADO: ',titulo_pro)

#         titulo_pal = titulo_pro.split()
#         print('PALABRAS TITULO: ',titulo_pal)
#         for titulo in titulo_pal:
#             if len(titulo)>4:
#                 print(len(titulo))

#         print('=========================================================================================================')
#     except AttributeError:
#         print('OPINIÓN')
#         print('=========================================================================================================')

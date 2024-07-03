from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import calendar
import os
import re

class program:
    def __init__(self):
        # VARIABLES GLOBALES
        self.year= ["2020","2021","2022"]
        self.months = ['01','02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.cover = ["m","t","n"]
        self.urlBase= "https://elpais.com/hemeroteca/elpais/"
        self.urlBase2= "https://static.elpais.com/hemeroteca/elpais/"
        self.filter = ["coronavirus", "covid-19", "pandemia", "vacuna", "contagio", "cuarentena", "síntomas","confinamiento", "distanciamiento", "cierre",
                "contagios","contagio", "virus", "wuhan", "epidemia", "brote","brotes", "aislamiento", "sars-cov-2", "transmisión", "variante", "variantes",
                "cepa", "mascarilla", "uci", "teletrabajo"]
        self.datePattern = r"/(\d{4})/(\d{2})/(\d{2})/" #YYYY/MM/DD
        self.datePattern2 = r"/(\d{4})-(\d{2})-(\d{2})/" #YYYY-MM-DD
        # Change when the checkpoint day is greater than 2020/05/11/t
        self.isStatic= False

        # CACHE TO AVOID ACCESSING THE SAME NEWS MORE THAN ONCE
        self.cacheTitles = []

        # RESULTS
        self.newsList = []

        # EXECUTION
        self.run()

    def run(self):
        # Load checkpoint information if it exists
        checkpoint_info = self.load_checkpoint()
        start_year = checkpoint_info.get("year", "2020")
        start_month = checkpoint_info.get("month", "01")

        # Driver preparation
        opts = Options()
        opts.add_argument('--log-level=3') 
        opts.add_experimental_option('excludeSwitches', ['enable-automation'])
        opts.add_experimental_option('useAutomationExtension', False)
        opts.add_argument('--disable-javascript')
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36") #Buscar el user-agent

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opts
        )

        for y in self.year[self.year.index(start_year):]:
            for m in self.months[self.months.index(start_month):]:
                lastDay = calendar.monthrange(int(y), int(m))[1]
        
                # Adjust range for leap years
                if calendar.isleap(int(y)) and m == "02":
                    monthDays = [str(d).zfill(2) for d in range(1, lastDay + 1)]
                else:
                    monthDays = [str(d).zfill(2) for d in range(1, lastDay)]

                for d in monthDays:
                    for p in self.cover:
                        if self.isStatic:
                            url2 = f"{self.urlBase2}{y}/{m}/{d}/{p}/portada.html"
                            program.news2(self, driver, url2)
                        else:
                            url = f"{self.urlBase}{y}/{m}/{d}/{p}/portada.html"
                            if url != "https://elpais.com/hemeroteca/elpais/2020/05/11/n/portada.html":
                                program.news(self, driver, url)
                            else:
                                date= f'_{y}-{m}-{d}-{p}'
                                program.writeJson(self,date)
                                self.newsList.clear()
                                url2 = f"{self.urlBase2}{y}/{m}/{d}/{p}/portada.html"
                                program.news2(self, driver, url2)
                                self.isStatic= True
                #JSON
                date= f'_{y}-{m}'
                program.writeJson(self,date)
                self.cacheTitles.clear()
                self.newsList.clear()
                
                # Update checkpoint
                self.update_checkpoint(y, m)

        driver.quit()

    # FUNCTIONS
    def news(self, driver, url):
        driver.delete_all_cookies()
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, features='html.parser')
        titles = soup.find_all('h2', class_='articulo-titulo')
        program.newArticle(self, titles, driver)

    def news2(self, driver, url2):
        driver.delete_all_cookies()
        driver.get(url2)
        html = driver.page_source
        soup = BeautifulSoup(html, features='html.parser')
        titles = soup.find_all('h2', class_='headline').get_text(strip=True)
        program.newArticle(self, titles, driver)
        
    def newArticle(self, news, driver):
        for new in news:
            title = new.text
            if title not in self.cacheTitles:
                titlePro = title.lower().replace(".", "")
                titleWords = titlePro.split()

                if program.themeInTitle(self, titleWords): # "FILTER"
                    newsDict = dict()
                    newsDict['Título'] = title
                    
                    #Link treatmen
                    try:
                        link = new.find('a')['href']
                        
                        driver.delete_all_cookies()
                        driver.get(link)
                    

                        newHtml = driver.page_source
                        newSoup = BeautifulSoup(newHtml, features='html.parser')
                        
                        newsDict['Cuerpo'] = program.inArticle(newSoup, link)
                        newsDict['Enlace'] = link

                        newsDict['Fecha'] = program.dateInLink(self, link)

                        self.newsList.append(newsDict)
                    except:
                        pass

                self.cacheTitles.append(title)

    def inArticle(soup, link):
        if link.startswith('https://motor.elpais.com'):
            subtitle = soup.find('h2', class_='entry-header__subtitulo').get_text(strip=True)
            body = soup.find('div', class_='content__main__content').get_text(strip=True)
            return f'{subtitle}. {body}'
        elif link.startswith('https://as.com/meristation/'):
            subtitle = soup.find('h2', class_='art__hdl__opn').get_text(strip=True)
            body = soup.find('div', class_='art__bo is-unfolded').get_text(strip=True)
            return f'{subtitle}. {body}'

        elif link.startswith('https://verne.elpais.com/verne'):
            subtitle = soup.find('h2', class_='subtitulo').get_text(strip=True)
            body = soup.find('div', class_='cuerpo').get_text(strip=True)
            return f'{subtitle}. {body}'
        elif link.startswith('https://cadenaser.com'):
            subtitle = soup.find('h2').get_text(strip=True)
            body = soup.find('div', class_='cnt-data-art').get_text(strip=True)
            return f'{subtitle}. {body}'
        elif link.startswith('https://www.huffingtonpost.es'):
            try:
                body = soup.find('div', class_='c-detail__body').get_text(strip=True)
                return body
            except:
                print('ERROR en: ', link)
                return "Error al obtener el contenido"
        else:
            try:
                subtitle = soup.find('h2', class_='a_st').get_text(strip=True)
                body = soup.find('div', class_='a_c clearfix').get_text(strip=True)
                return f'{subtitle}. {body}'
            except:
                print('ERROR en: ', link)
                return "Error al obtener el contenido"
    
    def themeInTitle(self ,titleWords):
        for title in titleWords:
            if len(title)>4 and title in self.filter :
                return True
        return False
    def dateInLink(self, link):
        result = re.search(self.datePattern, link)
        if result:
            year = result.group(1)
            month = result.group(2)
            day = result.group(3)
            date = f"{day}/{month}/{year}"
            return date
        else:
            result2 = re.search(self.datePattern2, link)
            if result2:
                year = result2.group(1)
                month = result2.group(2)
                day = result2.group(3)
                date = f"{day}/{month}/{year}"
                return date
            else:
                return "Fecha por estimar"
    
    def writeJson(self, date):
        pathJson = f'D:\Carrera\TFG\Pruebas de código\Extraccion\jsons\El pais\ELPAISV4\datos{date}.json'
        
        with open(pathJson, 'w', encoding='utf-8') as jsonFile:
            json.dump(self.newsList, jsonFile, ensure_ascii=False, indent=4)

        print(f"News saved in JSON format, {pathJson}")

    def load_checkpoint(self):
        checkpoint_file = 'D:\Carrera\TFG\Pruebas de código\Extraccion\checkpoint\checkpoint_paisFINAL.json'
        if os.path.exists(checkpoint_file):
            with open(checkpoint_file, 'r') as f:
                return json.load(f)
        return {}

    def update_checkpoint(self, current_year, current_month):
        checkpoint_info = {"year": current_year, "month": current_month}
        checkpoint_file = 'D:\Carrera\TFG\Pruebas de código\Extraccion\checkpoint\checkpoint_paisFINAL.json'
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_info, f)

if __name__ == '__main__':
    program()
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
        # GLOBAL VARIABLES
        self.years= ["2020","2021","2022"]
        self.months = ['01','02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.urlBase= "https://www.libertaddigital.com/"
        self.filters = ["coronavirus", "covid-19", "pandemia", "vacuna", "contagio", "cuarentena", "síntomas","confinamiento", "distanciamiento", "cierre",
                "contagios","contagio", "virus", "wuhan", "epidemia", "brote","brotes", "aislamiento", "sars-cov-2", "transmisión", "variante", "variantes",
                "cepa", "mascarilla", "uci", "teletrabajo"]

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
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opts
        )

        for y in self.years[self.years.index(start_year):]:
            for m in self.months[self.months.index(start_month):]:
                lastDay = calendar.monthrange(int(y), int(m))[1]
        
                # Adjust range for leap years
                if calendar.isleap(int(y)) and m == "02":
                    monthDays = [str(d).zfill(2) for d in range(1, lastDay + 1)]
                else:
                    monthDays = [str(d).zfill(2) for d in range(1, lastDay)]

                for d in monthDays:
                    url = f"{self.urlBase}{y}-{m}-{d}/"
                    program.news(self, driver, url)

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
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, features='html.parser')
        news = soup.find_all("article", class_='noticia centrado conimagen')
        news2 = soup.find_all("article", class_='noticia conimagen')
        news3 = soup.find_all("article", class_='noticia centrado')
        # concatenated the news
        news+=news2+news3
        program.newArticle(self, news, driver)

    def newArticle(self, news, driver):
        for new in news:
            title = new.find('h2').get_text(strip=True)
            if title not in self.cacheTitles:
                titlePro = title.lower().replace(".", "")

                titleWords = titlePro.split()

                if program.themeInTitle(self, titleWords): # "FILTER"
                    link = new.find('a')['href']
                    newsDict = dict()
                    newsDict['Título'] = title

                    driver.delete_all_cookies()
                    driver.get(link)
                    newHtml = driver.page_source
                    newSoup = BeautifulSoup(newHtml, features='html.parser')
                    try:
                        newsDict['Cuerpo'] = newSoup.find('div', class_='body').get_text(strip=True)
                    except Exception as  e:
                        newsDict['Cuerpo'] = "Error al obtener el contenido"
                        print("Error al procesar la noticia: ", e)
                        print("ENLACE: ", link)
                        print("==============================================")

                    newsDict['Enlace'] = link
                    self.newsList.append(newsDict)

                self.cacheTitles.append(title)
    
    def themeInTitle(self ,titleWords):
        for title in titleWords:
            if len(title)>4 and title in self.filters :
                return True
        
        return False
    
    def writeJson(self, date):
        pathJson = f'D:\Carrera\TFG\Pruebas de código\Extraccion\jsons\Libertad digital\datos{date}.json'
        with open(pathJson, 'w', encoding='utf-8') as jsonFile:
            json.dump(self.newsList, jsonFile, ensure_ascii=False, indent=4)

        print(f"News saved in JSON format, {pathJson}")

    def load_checkpoint(self):
        checkpoint_file = 'D:\Carrera\TFG\Pruebas de código\Extraccion\checkpoint\checkpoint_libertad-digital.json'
        if os.path.exists(checkpoint_file):
            with open(checkpoint_file, 'r') as f:
                return json.load(f)
        return {}

    def update_checkpoint(self, current_year, current_month):
        checkpoint_info = {"year": current_year, "month": current_month}
        checkpoint_file = 'D:\Carrera\TFG\Pruebas de código\Extraccion\checkpoint\checkpoint_libertad-digital.json'
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_info, f)

if __name__ == '__main__':
    program()

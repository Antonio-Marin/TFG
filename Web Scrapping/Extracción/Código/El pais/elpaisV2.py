from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import calendar
import os
import sys

class program:
    def __init__(self):
        # VARIABLES GLOBALES
        self.year= ["2021","2022"]
        self.months = ['01','02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.cover = ["m","t","n"]
        self.urlBase= "https://static.elpais.com/hemeroteca/elpais/"
        self.filter = ["coronavirus", "covid-19", "pandemia", "vacuna", "contagio", "cuarentena", "síntomas","confinamiento", "distanciamiento", "cierre",
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
        start_year = checkpoint_info.get("year", "2022") 
        start_month = checkpoint_info.get("month", "12")  

        # Driver preparation
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36") #Buscar el user-agent

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opts
        )

        for y in reversed(self.year[:self.year.index(start_year) + 1]):
            for m in reversed(self.months[:self.months.index(start_month) + 1]):
                lastDay = calendar.monthrange(int(y), int(m))[1]
        
                # Adjust range for leap years
                if calendar.isleap(int(y)) and m == "02":
                    monthDays = [str(d).zfill(2) for d in reversed(range(1, lastDay + 1))]
                else:
                    monthDays = [str(d).zfill(2) for d in reversed(range(1, lastDay + 1))]

                for d in monthDays:
                    for p in self.cover:
                        if f"{y}/{m}/{d}" == "2021/09/30":
                            sys.exit()
                        url = f"{self.urlBase}{y}/{m}/{d}/{p}/portada.html"
                        program.news2(self, driver, url)
                #JSON
                date= f'_{y}-{m}'
                program.writeJson(self,date)
                self.cacheTitles.clear()
                self.newsList.clear()
                
                # Update checkpoint
                self.update_checkpoint(y, m)

        driver.quit()

    # FUNCTIONS
    def news2(self, driver, url):
        driver.get(url)
        driver.delete_all_cookies()
        html = driver.page_source
        soup = BeautifulSoup(html, features='html.parser')
        titles = soup.find_all('h2', class_='c_t')
        program.newArticle(self, titles)
        
    def newArticle(self, news):
        for new in news:
            title = new.text
            if title not in self.cacheTitles:
                titlePro = title.lower().replace(".", "")
                titleWords = titlePro.split()

                if program.themeInTitle(self, titleWords): # "FILTRO"
                    newsDict = dict()
                    newsDict['Título'] = title
                    link = new.a['href']
                    if (link.startswith("/")):
                        newsDict['Enlace'] = f'https://elpais.com{link}'
                    else:
                        newsDict['Enlace'] = link 

                    self.newsList.append(newsDict)

                self.cacheTitles.append(title)
    
    def themeInTitle(self ,titleWords):
        for title in titleWords:
            if len(title)>4 and title in self.filter :
                return True
        return False
    
    def writeJson(self, date):
        pathJson = f'D:\Carrera\TFG\Pruebas de código\Extraccion\jsons\El pais\datos{date}.json'
        with open(pathJson, 'w', encoding='utf-8') as jsonFile:
            json.dump(self.newsList, jsonFile, ensure_ascii=False, indent=4)

        print(f"News saved in JSON format, {pathJson}")

    def load_checkpoint(self):
        checkpoint_file = 'D:\Carrera\TFG\Pruebas de código\Extraccion\checkpoint\checkpoint_pais.json'
        if os.path.exists(checkpoint_file):
            with open(checkpoint_file, 'r') as f:
                return json.load(f)
        return {}

    def update_checkpoint(self, current_year, current_month):
        checkpoint_info = {"year": current_year, "month": current_month}
        checkpoint_file = 'D:\Carrera\TFG\Pruebas de código\Extraccion\checkpoint\checkpoint_pais.json'
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_info, f)

if __name__ == '__main__':
    program()
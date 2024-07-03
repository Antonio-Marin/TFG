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
        self.cover = ["m","t","n"]
        self.urlBase= "https://www.elmundo.es/elmundo/hemeroteca/"
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
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36") #Buscar el user-agent

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
                    for p in self.cover:
                        url = f"{self.urlBase}{y}/{m}/{d}/{p}"
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
        news = soup.find_all('header', class_='ue-c-cover-content__headline-group')
        program.newArticle(self, news, driver)

    def newArticle(self, news, driver):
        for new in news:
            try:
                title = new.find('a', class_='ue-c-cover-content__link').text
                if title not in self.cacheTitles:
                    topic = new.find('span', class_='ue-c-cover-content__kicker').text
                    topicPro = topic.lower().replace(" ", "").replace(".", "")
                    titlePro = title.lower().replace(".", "")

                    titleWords = titlePro.split()

                    if topicPro  in self.filters or program.themeInTitle(self, titleWords): # "FILTER"
                        link = new.find('a', class_='ue-c-cover-content__link')['href']
                        newsDict = dict()

                        newsDict['Tema'] = topic
                        newsDict['Título'] = title

                        driver.get(link)
                        newHtml = driver.page_source
                        newSoup = BeautifulSoup(newHtml, features='html.parser')
                        newsDict['Cuerpo'] = program.inArticle(newSoup)
                        newsDict['Enlace'] = link
                        self.newsList.append(newsDict)

                    self.cacheTitles.append(title)

            except AttributeError:
                # Non-news articles
                pass
            
    def inArticle(soup):
        newSubtitle = soup.find('p', class_='ue-c-article__standfirst').text
        newsBody = soup.find_all('div', class_='ue-l-article__body ue-c-article__body')
        aux = ""
        for element in newsBody:
            paragraphs = element.find_all('p')
            for paragraph in paragraphs:
                if paragraph.text != "Conforme a los criterios deThe Trust Project":
                    aux+= paragraph.text
        return f'{newSubtitle}. {aux}'
    
    def themeInTitle(self ,titleWords):
        for title in titleWords:
            if len(title)>4 and title in self.filters :
                return True
        
        return False
    
    def writeJson(self, date):
        pathJson = f'D:\Carrera\TFG\Pruebas de código\Extraccion\jsons\El mundo\datos{date}.json'
        with open(pathJson, 'w', encoding='utf-8') as jsonFile:
            json.dump(self.newsList, jsonFile, ensure_ascii=False, indent=4)

        print(f"News saved in JSON format, {pathJson}")

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

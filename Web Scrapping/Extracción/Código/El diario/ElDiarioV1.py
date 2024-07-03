from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os

class program:
    def __init__(self):
        # GLOBAL VARIABLES
        self.urlBase= "https://www.eldiario.es/busqueda/"
        self.year = ["2020", "2021", "2022"]
        #DONE "coronavirus", "covid-19", "pandemia", "vacuna", "contagio", "cuarentena", "síntomas","confinamiento", "distanciamiento", "cierre","contagios"
        # "virus", "wuhan", "epidemia", "brote", "aislamiento", "sars-cov-2","transmisión", "variante", "cepa", "mascarilla", "uci", "teletrabajo",
        self.searchs = [ "vacunación", "tratamiento", "restricciones", "inmunidad"]
                
        # CACHE TO AVOID ACCESSING THE SAME NEWS MORE THAN ONCE
        self.cacheTitles = []

        # RESULTS
        self.newsList = []

        # EXECUTION
        self.run()
    
    def run(self):

        for search in self.searchs:
            # Driver preparation
            print("Palabra a buscar: ",search)
            opts = Options()
            opts.add_argument('--log-level=3') 
            opts.add_experimental_option('excludeSwitches', ['enable-automation'])
            opts.add_experimental_option('useAutomationExtension', False)
            opts.add_argument('--disable-javascript')
            opts.add_argument("--no-sandbox")
            opts.add_argument("--headless")
            opts.add_argument("--disable-gpu")
            opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36")
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=opts
            )

            url = f'{self.urlBase}{search}'
            program.loadArticles(self, url, driver)
            program.writeJson(self,search)
            self.newsList.clear()
            self.cacheTitles.clear()
            driver.quit()
        
    def loadArticles(self, url, driver):
        driver.delete_all_cookies()
        driver.get(url)

        buttonCookies = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "didomi-notice-agree-button"))
        )
        buttonCookies.click()

        maxClicks = 10
        clickCount = 0
        while clickCount < maxClicks:
            try:
                print("clickCount: ", clickCount)
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "view-more-button"))
                )
                next_button.click()
                clickCount+=1
            except:
                print("No more news.\n")
                break
        html = driver.page_source
        program.articles(self, html, driver)
    
    def articles(self, html, driver):
        soup = BeautifulSoup(html, features='html.parser')
        news = soup.find_all("li", class_="article-cont-search")
        for new in news:
            date = new.find("time").get_text(strip=True)
            if program.containYear(self, date):
                title = new.find("div", class_="second-column")
                if title not in self.cacheTitles:
                    topic = new.find("a").get_text(strip=True)
                    title = new.find("div", class_="second-column")
                    link = title.find("a")['href']
                    try:
                        driver.delete_all_cookies()       
                        driver.get(link)
                        newHtml = driver.page_source
                        articleSoup = BeautifulSoup(newHtml, features='html.parser')
                        body = articleSoup.find('div', class_='partner-wrapper article-page__body-row').get_text(strip=True)
                        newsDict = dict()
                        newsDict['Título'] = f'{topic.lstrip("elDiario.es ")}. {title.get_text(strip=True).rstrip("0")}'
                        newsDict['Cuerpo'] = body
                        newsDict['Enlace'] = link
                        newsDict['Fecha'] = date
                        self.newsList.append(newsDict)
                        print("Title: ", newsDict['Título'])
                    except Exception as e:
                        print("Error getting the body of the news:", link)
                        print("Beacuse: ", e )

                    self.cacheTitles.append(title)
    
    def containYear(self, date):
        for year in self.year:
            if year in date:
                return True
        return False
    def writeJson(self, search):
        pathJson = f'D:\Carrera\TFG\Pruebas de código\Extraccion\jsons\El diario\datos_{search}.json'
        with open(pathJson, 'w', encoding='utf-8') as jsonFile:
            json.dump(self.newsList, jsonFile, ensure_ascii=False, indent=4)

        print(f"News saved in JSON format, {pathJson}")

if __name__ == '__main__':
    program()
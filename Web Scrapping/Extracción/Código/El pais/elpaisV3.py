from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import os

class program:
    def __init__(self):
        self.path = "D:/Carrera/TFG/Pruebas de código/Extraccion/jsons/El pais/"
        self.year= ["2020","2021","2022"]
        self.months = ['01','02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.newsList = []
        program.run(self)

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
        
        for y in self.year[self.year.index(start_year):]:
            for m in self.months[self.months.index(start_month):]:
                name = f'datos_{y}-{m}'
                data = program.openJson(self,name)
                program.processData(self,data, driver)
                program.writeJson(self,name)
                self.newsList.clear()
                self.update_checkpoint(y, m)
        driver.quit()

    def processData(self,data, driver):
        counter = 0
        for new in data:
            newsDict = dict()
            title = new['Título'].strip()
            link = new['Enlace']
            newsDict['Título'] = title
            if not 'Cuerpo' in new:
                driver.delete_all_cookies()
                driver.get(link)
                print(link)
                html = driver.page_source
                soup = BeautifulSoup(html, features='html.parser')
                if link.startswith('https://motor.elpais.com'):
                    subtitle = soup.find('h2', class_='entry-header__subtitulo').get_text(strip=True)
                    body = soup.find('div', class_='content__main__content').get_text(strip=True)
                    newsDict['Cuerpo'] = f'{subtitle}. {body}'
                elif link.startswith('https://as.com/meristation/'):
                    subtitle = soup.find('h2', class_='art__hdl__opn').get_text(strip=True)
                    body = soup.find('div', class_='art__bo is-unfolded').get_text(strip=True)
                    newsDict['Cuerpo'] = f'{subtitle}. {body}'
                elif link.startswith('https://verne.elpais.com/verne'):
                    subtitle = soup.find('h2', class_='subtitulo').get_text(strip=True)
                    body = soup.find('div', class_='cuerpo').get_text(strip=True)
                    newsDict['Cuerpo'] = f'{subtitle}. {body}'
                elif link.startswith('https://www.huffingtonpost.es'):
                    try:
                        body = soup.find('div', class_='c-detail__body').get_text(strip=True)
                        newsDict['Cuerpo'] = body
                    except:
                        counter+=1
                        newsDict['Cuerpo'] = "Error al obtener el contenido"
                        print(counter, '. ERROR en: ', link)
                else:
                    try:
                        subtitle = soup.find('h2', class_='a_st').get_text(strip=True)
                        body = soup.find('div', class_='a_c clearfix').get_text(strip=True)
                        newsDict['Cuerpo'] = f'{subtitle}. {body}'
                    except:
                        counter+=1
                        newsDict['Cuerpo'] = "Error al obtener el contenido"
                        print(counter, '. ERROR en: ', link)

            else:
                newsDict['Cuerpo'] = new['Cuerpo']
            newsDict['Enlace'] =  link
            self.newsList.append(newsDict)
    
    def openJson(self,name):
        pathJson = f'{self.path}{name}.json'
        with open(pathJson, encoding='utf-8' ) as jsonFile:
            dataJson = json.load(jsonFile)
        return dataJson
    
    def writeJson(self, name):
        pathJson = f'D:\Carrera\TFG\Pruebas de código\Extraccion\jsons\El pais FINAL\{name}.json'
        with open(pathJson, 'w', encoding='utf-8') as jsonFile:
            json.dump(self.newsList, jsonFile, ensure_ascii=False, indent=4)
        print(f"News saved in JSON format, {pathJson}")
        print('-------------------------------')
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
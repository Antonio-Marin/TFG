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

driver.get('https://www.libertaddigital.com/2020-01-01/')
# driver.get('https://www.libertaddigital.com/espana/politica/2020-01-01/solo-18-votantes-psoe-respalda-dialogo-separatismo-fuera-constitucion-1276650187/')

html = driver.page_source
soup = BeautifulSoup(html, features='html.parser')
#body = soup.find('div', class_='body').get_text(strip=True) 
#print(body)
articles = soup.find_all("article", class_='noticia centrado conimagen')
articles2 = soup.find_all("article", class_='noticia conimagen')
articles3 = soup.find_all("article", class_='noticia centrado')
articles+=articles2+articles3
cont = 1
for article in articles:
    print('ARTICULO',cont,': ', article.find('h2').get_text(strip=True))
    print('Enlace: ', article.find('a')['href'])
    print('====================================================')
    cont+=1
# for article in articles2:
#     print('ARTICULO',cont,': ', article.find('h2').get_text(strip=True))
#     print('Enlace: ', article.find('a')['href'])
#     print('====================================================')
#     cont+=1

driver.quit()
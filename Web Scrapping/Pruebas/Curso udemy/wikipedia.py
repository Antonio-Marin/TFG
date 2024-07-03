import requests

from lxml import html

from bs4 import BeautifulSoup
import re

url ="https://www.wikipedia.org/"
encabezado = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"

}

content = requests.get(url, headers=encabezado)
#print(content.text)

parser = html.fromstring(content.text)

español = parser.get_element_by_id("js-link-box-es")
#print(español.text_content())

español2 = parser.xpath("//a[@id='js-link-box-es']/strong/text()")
#print(español2)

## Probado por mi cuenta, a mi parecer mucho mas facil y menos lio
soup = BeautifulSoup(content.text, features="html.parser")
result=soup.find("a", id="js-link-box-es")
#print("Forma 1: ", result.find("strong").text)
#print("Forma 2: ", result.findChild().text)
#print("Forma 3: ",result.find_next().text)
##

## Nombres idiomas
langs=soup.select(".central-featured-lang strong")
#print(langs)



import pyautogui as bot
import requests
from bs4 import BeautifulSoup
import re

#URL da página da Scielo
url = "https://www.scielo.br/j/anp/i/1943.v1n1/"

#Acessando a página por meio de solicitação HTTP
response = requests.get(url)

#Verifica se a requisição foi bem-sucedida comparando com 200, ou seja, OK
if response.status_code == 200:
    #Transforma o conteúdo HTML do site usando o BeatifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    artigos = soup.find_all('ul', class_='links')

    count = 0

    for artigo in artigos:
        count += 1
        link = artigo.find('a')
        
        estilo = artigo.get('style')
        coordenada_x = re.search(r'left:(\d+)px', estilo).group(1)
        coordenada_y = re.search(r'top:(\d+)px', estilo).group(1)

        print(count, "= x:", coordenada_x,"y:", coordenada_y)
        
    print("O número de artigos na página é:", count)
        

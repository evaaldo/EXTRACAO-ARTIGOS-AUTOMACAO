import pyautogui as bot
import requests
from bs4 import BeautifulSoup

#URL da página da Scielo
url = "https://www.scielo.br/j/anp/i/1943.v1n1/"

#Acessando a página por meio de solicitação HTTP
response = requests.get(url)

#Verifica se a requisição foi bem-sucedida comparando com 200, ou seja, OK
if response.status_code == 200:
    #Transforma o conteúdo HTML do site usando o BeatifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    artigos = soup.find_all('div', class_='articles')

    print("ta dando bao")

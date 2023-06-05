from bs4 import BeautifulSoup
import requests

#URL da página da Scielo
URL = "https://www.scielo.br/j/anp/a/z9dRGTnDrPgjWkS7cvgyLHw/?lang=en"

#Acessando a página por meio da requisição HTTP
response = requests.get(URL)

#Verifica se a requisição foi bem-sucedida comparando com 200, ou seja, OK
if(response.status_code == 200):

    #Transforma o conteúdo HTML do site usando o BeatifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    #Informações buscadas
    ano = soup.find_all('span', class_='_editionMeta')
    anoConteudo = ano.text.strip()

    print("Conectou legal")
    print(anoConteudo)

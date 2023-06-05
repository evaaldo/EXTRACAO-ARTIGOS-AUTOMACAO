from bs4 import BeautifulSoup
import requests
import re

#URL da página da Scielo
URL = "https://www.scielo.br/j/anp/a/z9dRGTnDrPgjWkS7cvgyLHw/?format=html&lang=en&stop=previous"

#Acessando a página por meio da requisição HTTP
response = requests.get(URL)

#Verifica se a requisição foi bem-sucedida comparando com 200, ou seja, OK
if(response.status_code == 200):

    #Transforma o conteúdo HTML do site usando o BeatifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    #Arrays
    anos = []
    fasciculos = []
    titulos = []

    #Informações buscadas
    ano = soup.find('span', class_='_editionMeta')
    fasciculo = soup.find('span', class_='_editionMeta')
    tituloIngles = soup.find('h1', class_='article-title')
    tituloPortugues = soup.find('h2', class_='article-title')

    #Isso tudo deve estar dentro de um loop

    ano_conteudo = ano.text.strip()
    fasciculo_conteudo = fasciculo.text.strip()
    tituloIngles_conteudo = tituloIngles.text.strip()
    tituloPortugues_conteudo = tituloPortugues.text.strip()

    #Códigos para informações que precisam de padrão Regex
    padrao_fasciculo = re.compile(r'\((.*?)\)')

    #Valor esperado
    ano_conteudo = ano_conteudo.split("•")[-1].strip()
    fasciculo_conteudo = re.findall(padrao_fasciculo, fasciculo_conteudo)
    fasciculo_conteudo = fasciculo_conteudo[0].strip()
    
    #Armazenamento
    anos.append(ano_conteudo)
    fasciculos.append(fasciculo_conteudo)

    #Condicional necessária para os títulos, porém ainda faz parte da etapa de armazenamento
    if(tituloPortugues_conteudo == ''):
        titulos.append(tituloIngles_conteudo)
    else:
        titulos.append(tituloPortugues_conteudo)
    
    

    print("Conectou legal")
    print(anos)
    print(fasciculos)
    print(titulos)

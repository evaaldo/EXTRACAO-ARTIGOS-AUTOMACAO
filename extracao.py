from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

# #Inicializa o driver do Selenium
# driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
# driver.get("https://www.scielo.br/j/anp/a/z9dRGTnDrPgjWkS7cvgyLHw/?format=html&lang=en&stop=previous")

#URL da página da Scielo
URL = "https://www.scielo.br/j/anp/a/YNp5dkZn7ckhbSWXv7bcSwv/?lang=pt"

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
    # citacoes = []
    nomesPrimeiroAutor = []
    # nomesCorrespondenteAutor = []
    paisesPrimeiroAutor = []

    #Informações buscadas com BeatifulSoup
    ano = soup.find('span', class_='_editionMeta')
    fasciculo = soup.find('span', class_='_editionMeta')
    tituloIngles = soup.find('h1', class_='article-title')
    tituloPortugues = soup.find('h2', class_='article-title')
    citacaoLista = soup.find_all('ul', class_='refList')
    autoresDiv = soup.find('div', class_='tutors')
    autorPrincipal = autoresDiv.find('strong')
    # autorCorrespondenteDiv = soup.find('ul', class_='footnote')
    # # autorCorrespondente = autorCorrespondenteDiv.find('li')

    #Isso tudo deve estar dentro de um loop
    #LOOP AQUI!!

    #Extração de textos
    ano_conteudo = ano.text.strip()
    fasciculo_conteudo = fasciculo.text.strip()
    tituloIngles_conteudo = tituloIngles.text.strip()
    tituloPortugues_conteudo = tituloPortugues.text.strip()
    autorPrincipal_conteudo = autorPrincipal.text.strip()
    # # autorCorrespondente_conteudo = autorCorrespondente.text.strip()

    if autoresDiv:
        # Extração do texto 
        paisPrimeiroAutor = autoresDiv.get_text(separator=',')

        # Divide o texto pelo separador vírgula
        partes = paisPrimeiroAutor.split(',')

        # Verifica se existem pelo menos duas partes separadas por vírgula
        if len(partes) >= 2:
            # Obtém o texto após a penúltima parte
            paisPrimeiroAutor_conteudo = ','.join(partes[-8:-5])

    #loop necessário para capturar o número de informações, porém ainda faz parte da etapa de extração de textos
    #Checa cada <li> dentro da <ul>
    for citacao in citacaoLista:
        #identifica as tags <li>
        tags_li = citacao.find_all('li')

        #Verifica se há tags <li>
        if tags_li:
            #Indica qual a última tag <li>
            ultima_tag_li = tags_li[-1]

            #Indica a tag <sup> dentro da última tag <li>
            tag_sup = ultima_tag_li.find('sup')

            #Verifica se há uma tag <sup>
            # if tag_sup:
                #Indica o valor da última tag <sup>, ou seja, o número de citações
                # num_citacoes = int(tag_sup.text.strip())

    

    #Códigos para informações que precisam de padrão Regex
    padrao_fasciculo = re.compile(r'\((.*?)\)')
    # padrao_autorCorrespondente = r'Address for correspondence (.+?) \(email'

    #Valor esperado
    ano_conteudo = ano_conteudo.split("•")[-1].strip()
    fasciculo_conteudo = re.findall(padrao_fasciculo, fasciculo_conteudo)
    fasciculo_conteudo = fasciculo_conteudo[0].strip()
    # # # autorCorrespondente_conteudo = re.findall(padrao_autorCorrespondente, autorCorrespondente_conteudo)
    # # autorCorrespondente_conteudo = autorCorrespondente_conteudo[0].strip()
    # # autorCorrespondente_conteudo = autorCorrespondente_conteudo.replace(',', '')
    
    #Armazenamento
    anos.append(ano_conteudo)
    fasciculos.append(fasciculo_conteudo)
    nomesPrimeiroAutor.append(autorPrincipal_conteudo)
    # # nomesCorrespondenteAutor.append(autorCorrespondente_conteudo)
    paisesPrimeiroAutor.append(paisPrimeiroAutor_conteudo)

    #Condicional necessária para os títulos, porém ainda faz parte da etapa de armazenamento
    if(tituloPortugues_conteudo == ''):
        titulos.append(tituloIngles_conteudo)
    else:
        titulos.append(tituloPortugues_conteudo)
    
    # # citacoes.append(num_citacoes)
    
    print("Lista de anos:", anos)
    print("Lista de fascículos:", fasciculos)
    print("Lista de títulos:", titulos)
    # print("Lista de citações:", citacoes)
    print("Lista de nomes de primeiro autor:", nomesPrimeiroAutor)
    # # print("Lista de nomes de autor correspondente:", nomesCorrespondenteAutor)
    print("Lista de países de primeiro autor:", paisesPrimeiroAutor)

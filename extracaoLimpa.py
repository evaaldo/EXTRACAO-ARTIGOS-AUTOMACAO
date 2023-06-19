from bs4 import BeautifulSoup
import requests
import re
from io import BytesIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import resolve1
import time

start_time = time.time()

# URL da página da Scielo
URL = "https://www.scielo.br/j/anp/a/sXXvxXsxvhfV6QSwDTy36Wg/?lang=en#"

pdf = 'https://www.scielo.br/j/anp/a/PqWg3NpT7zQYBgf6qvwTmtq/?format=pdf&lang=pt'

def extracao():

    # Acessando a página por meio da requisição HTTP
    response = requests.get(URL)

    # Verifica se a requisição foi bem-sucedida comparando com 200, ou seja, OK
    if response.status_code == 200:

        # Transforma o conteúdo HTML do site usando o BeatifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Arrays para armazenar os dados
        anos = []
        fasciculos = []
        titulos = []
        citacoes = []
        paginas = []
        nomesPrimeiroAutor = []
        nomesCorrespondenteAutor = []
        paisesPrimeiroAutor = []
        paisesCorrespondenteAutor = []

        # Informações buscadas com BeatifulSoup
        ano = soup.find('span', class_='_editionMeta')
        fasciculo = soup.find('span', class_='_editionMeta')
        tituloIngles = soup.find('h1', class_='article-title')
        tituloPortugues = soup.find('h2', class_='article-title')
        citacaoLista = soup.find_all('ul', class_='refList')
        autoresDiv = soup.find('div', class_='tutors')
        autorPrincipal = autoresDiv.find('strong')
        autorCorrespondenteDiv = soup.find('ul', class_='footnote')

        # Extração de textos
        ano_conteudo = ano.text.strip()
        fasciculo_conteudo = fasciculo.text.strip()
        tituloIngles_conteudo = tituloIngles.text.strip()
        tituloPortugues_conteudo = tituloPortugues.text.strip()
        autorPrincipal_conteudo = autorPrincipal.text.strip()

        if autoresDiv:
            # Extração do texto
            paisPrimeiroAutor = autoresDiv.get_text(separator=',')

            # Divide o texto pelo separador vírgula
            partes = paisPrimeiroAutor.split(',')

            # Verifica se existem pelo menos duas partes separadas por vírgula
            if len(partes) >= 2:
                # Obtém o texto após a penúltima parte
                paisPrimeiroAutor_conteudo = ','.join(partes[-8:-5])

        # Extração completa do autor correspondente, caso ele exista
        if autorCorrespondenteDiv:
            # Identifica o item de uma lista
            autorCorrespondente = autorCorrespondenteDiv.find('li')

            # Extrai o texto do item identificado
            autorCorrespondente_conteudo = autorCorrespondente.text.strip()

            # Padrões de expressões regulares
            padrao_correspondencia_email = r'Address for correspondence (.+?) \(email'
            padrao_correspondencia = r'Correspondence: (.+?);'

            # Busca por correspondência usando os padrões nas strings relevantes
            correspondencia_email = re.findall(padrao_correspondencia_email, autorCorrespondente_conteudo)
            correspondencia = re.findall(padrao_correspondencia, autorCorrespondente_conteudo)

            # Verifica se encontrou correspondência usando o primeiro padrão
            if correspondencia_email:
                texto_correspondencia = correspondencia_email[0]
            # Verifica se encontrou correspondência usando o segundo padrão
            elif correspondencia:
                texto_correspondencia = correspondencia[0]
            else:
                texto_correspondencia = None

            # Armazena o valor caso exista
            if texto_correspondencia:
                nomesCorrespondenteAutor.append(texto_correspondencia.strip())

            if texto_correspondencia:
                primeiro_nome_correspondente = texto_correspondencia.split()[0]

                # Comparar com o primeiro nome do autor principal
                primeiro_nome_principal = autorPrincipal_conteudo.split()[0]

                # Armazenamento dos autores correspondentes
                if primeiro_nome_correspondente == primeiro_nome_principal:
                    paisesCorrespondenteAutor.append(paisPrimeiroAutor_conteudo)

        # loop necessário para capturar o número de informações, porém ainda faz parte da etapa de extração de textos
        # Checa cada <li> dentro da <ul>
        for citacao in citacaoLista:
            # Identifica as tags <li>
            tags_li = citacao.find_all('li')

            # Verifica se há tags <li>
            if tags_li:
                # Indica qual a última tag <li>
                ultima_tag_li = tags_li[-1]

                # Indica a tag <sup> dentro da última tag <li>
                tag_sup = ultima_tag_li.find('sup')

                # Verifica se há uma tag <sup>
                if tag_sup:
                    # Indica o valor da última tag <sup>, ou seja, o número de citações
                    num_citacoes = int(tag_sup.text.strip())

                    #Armazenamento do número de citações
                    citacoes.append(num_citacoes)

        # Códigos para informações que precisam de padrão Regex
        padrao_fasciculo = re.compile(r'\((.*?)\)')

        # Valor esperado
        ano_conteudo = ano_conteudo.split("•")[-1].strip()
        ano_conteudo = ano_conteudo[-4:]
        fasciculo_conteudo = re.findall(padrao_fasciculo, fasciculo_conteudo)
        fasciculo_conteudo = fasciculo_conteudo[0].strip()

        # Armazenamento
        anos.append(ano_conteudo)
        fasciculos.append(fasciculo_conteudo)
        nomesPrimeiroAutor.append(autorPrincipal_conteudo)
        paisesPrimeiroAutor.append(paisPrimeiroAutor_conteudo)

        # Condicional necessária para os títulos, porém ainda faz parte da etapa de armazenamento
        if tituloPortugues_conteudo == '':
            titulos.append(tituloIngles_conteudo)
        else:
            titulos.append(tituloPortugues_conteudo)

        # Faz o download do arquivo PDF
        response = requests.get(pdf)
        file_data = response.content

        # Cria um objeto BytesIO para representar o arquivo PDF em memória
        pdf_file = BytesIO(file_data)

        # Cria um objeto PDFParser para analisar o arquivo PDF
        parser = PDFParser(pdf_file)

        # Cria um objeto PDFDocument para representar o documento PDF
        document = PDFDocument(parser)

        # Obtém o número total de páginas
        total_pages = resolve1(document.catalog['Pages'])['Count']

        paginas.append(total_pages)

        print("Lista de anos:", anos)
        print("Lista de fascículos:", fasciculos)
        print("Lista de títulos:", titulos)
        print("Lista de nomes de primeiro autor:", nomesPrimeiroAutor)
        print("Lista de nomes de autor correspondente:", nomesCorrespondenteAutor)
        print("Lista de países de primeiro autor:", paisesPrimeiroAutor)
        print("Lista de países de autor correspondente:", paisesCorrespondenteAutor)
        print("Lista de número de citações:", citacoes)
        print("Lista de número de páginas:", paginas)
        


extracao()

end_time = time.time()

execution_time = end_time - start_time

print(f'Tempo de execução: {execution_time}')

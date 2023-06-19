from bs4 import BeautifulSoup
import requests
import re
import time
import PyPDF2

start_time = time.time()

# URL da página da Scielo
URL = "https://www.scielo.br/j/anp/a/4RHYpndvKwL63fGKDLMfb7c/?format=html&lang=pt"

links = [URL, URL]

# URL da página do PDF
pdf_url = 'https://www.scielo.br/j/anp/a/kxPBmT3bt67fjJycFQQ9fvf/?format=pdf&lang=en'

def extract_page_count(pdf_url):
    response = requests.get(pdf_url)
    with open('temp.pdf', 'wb') as f:
        f.write(response.content)

    with open('temp.pdf', 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        return len(pdf_reader.pages)

def extraction():
    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        anos = []
        fasciculos = []
        titulos = []
        nomesPrimeiroAutor = []
        nomesCorrespondenteAutor = []
        paisesPrimeiroAutor = []
        paisesCorrespondenteAutor = []
        citacoes = []
        paginas = []

        ano = soup.find('span', class_='_editionMeta').text.strip()
        fasciculo = soup.find('span', class_='_editionMeta').text.strip()

        tituloIngles = soup.find('h1', class_='article-title').text.strip()
        tituloPortugues = soup.find('h2', class_='article-title').text.strip() if soup.find('h2', class_='article-title') else ''

        autorPrincipal = soup.find('div', class_='tutors').find('strong').text.strip()
        autorCorrespondente = autorPrincipal[-1]

        autoresDiv = soup.find('div', class_='tutors')
        autorCorrespondenteDiv = soup.find('ul', class_='footnote')

        if autoresDiv:
            paisPrimeiroAutor = autoresDiv.get_text(separator=',')
            partes = paisPrimeiroAutor.split(',')

            if len(partes) >= 2:
                paisPrimeiroAutor_conteudo = ','.join(partes[-8:-5])

        if autorCorrespondenteDiv:
            autorCorrespondente = autorCorrespondenteDiv.find('li')
            autorCorrespondente_conteudo = autorCorrespondente.text.strip()

            padrao_correspondencia_email = r'Address for correspondence (.+?) \(email'
            padrao_correspondencia = r'Correspondence: (.+?);'

            correspondencia_email = re.findall(padrao_correspondencia_email, autorCorrespondente_conteudo)
            correspondencia = re.findall(padrao_correspondencia, autorCorrespondente_conteudo)

            texto_correspondencia = correspondencia_email[0] if correspondencia_email else correspondencia[0] if correspondencia else autorCorrespondente_conteudo

            if texto_correspondencia:
                nomesCorrespondenteAutor.append(texto_correspondencia.strip())

            if texto_correspondencia:
                primeiro_nome_correspondente = texto_correspondencia.split()[0]
                primeiro_nome_principal = autorPrincipal.split()[0]

                if primeiro_nome_correspondente == primeiro_nome_principal:
                    paisesCorrespondenteAutor.append(paisPrimeiroAutor_conteudo)

        citacaoLista = soup.find_all('ul', class_='refList')
        for citacao in citacaoLista:
            tags_li = citacao.find_all('li')
            num_citacoes = len(tags_li)
        citacoes.append(num_citacoes)


        padrao_fasciculo = re.compile(r'\((.*?)\)')
        ano_conteudo = ano.split("•")[-1].strip()[-4:]
        fasciculo_conteudo = re.findall(padrao_fasciculo, fasciculo)[0].strip()

        anos.append(ano_conteudo)
        fasciculos.append(fasciculo_conteudo)
        nomesPrimeiroAutor.append(autorPrincipal)
        paisesPrimeiroAutor.append(paisPrimeiroAutor_conteudo)

        if tituloPortugues == '':
            titulos.append(tituloIngles)
        else:
            titulos.append(tituloPortugues)

        total_pages = extract_page_count(pdf_url)
        paginas.append(total_pages)

        print("Lista de anos:", anos)
        print("Lista de fascículos:", fasciculos)
        print("Lista de títulos:", titulos)
        print("Lista de nomes de primeiro autor:", nomesPrimeiroAutor)
        print("Lista de países de primeiro autor:", paisesPrimeiroAutor)
        print("Lista de nomes de autor correspondente:", nomesCorrespondenteAutor)
        print("Lista de países de autor correspondente:", paisesCorrespondenteAutor)
        print("Lista de número de citações:", citacoes)
        print("Lista de número de páginas:", paginas)


extraction()

end_time = time.time()
execution_time = end_time - start_time
print(f'Tempo de execução: {execution_time} segundos')

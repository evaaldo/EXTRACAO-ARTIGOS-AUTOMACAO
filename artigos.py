import requests
from bs4 import BeautifulSoup
import time

initial_time = time.time()

URL = "https://www.scielo.br/j/anp/grid"

response = requests.get(URL)

paginas = []

if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')

    botoes = soup.select('table td.left a.btn')

    for botao in botoes:
        
        href = botao.get('href')
        paginas.append(href)
    
    print(len(paginas))

end_time = time.time()
execution_time = end_time - initial_time

print(execution_time)
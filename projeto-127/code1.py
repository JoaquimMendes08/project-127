from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd

#link do site
url = 'https://en.wikipedia.org/wiki/List_of_brightest_stars'

#coloque o endereço do chromedriver do seu computador
servico = webdriver.ChromeService(executable_path='C:\chromedriver-win64\chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=servico)
driver.get(url)

#tempo que o navegador mostrará o site
time.sleep(2)

#cria a lista das estrelas mais brilhantes
lista_estrelas = []

def scrape():
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #localize a tabela <table> com a classe jquery-tablesorter
    tabela = soup.find("table", attrs={"class":"jquery-tablesorter"})
    #nessa tabela, encontre o tbody
    table_tbody = tabela.find('tbody')
    #nesse tbody, encontre todas as linhas <tr> e adicione na variavel
    tabela_linhas = tabela.tbody.find_all("tr")

    #para cada uma das linhas, encontre as colunas
    for linha in tabela_linhas:
        #add as colunas <td> 
        tabela_colunas = linha.find_all("td")
        #crie a lista de dados
        lista = []

        #repita para cada coluna existente
        for coluna in tabela_colunas:
            #o método text() -> acessa os textos
            #o método strip() -> retira espaços brancos extras
            dado = coluna.text.split()
            #add o dado na lista
            lista.append(dado)
        
        #add a lista no dataframe
        lista_estrelas.append(lista)

#chame a função que coleta os dados do site
scrape()

#defina os títulos das colunas
headers = [
    'Rank', 'Visual magnitude', 'Proper Name', 
    'Bayer Designation','Distance', "Spectral type"
    ]

#converta em um dataframe
dataframe = pd.DataFrmae(lista_estrelas, column=headers)
#converta o dataframe em um arquivo csv
dataframe.to_csv("estrelas_mais_brilhantes")
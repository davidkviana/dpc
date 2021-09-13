#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Carregando as bibliotecas necessárias.
import json
import time
import process_data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

#next_table retorna as cidades caso exista uma nova página de municípios.
def next_table(driver):
    tb='/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table' #xpath da tabela alvo.
    table_id = driver.find_element(By.XPATH, tb)
    rows = table_id.find_elements(By.TAG_NAME, "tbody") #pega todas as linhas da tabela.
    cities = [] #armazena as cidades  be ceps encontrados.
    for row in rows:
        #pega todas as colunas da tabela alvo.
        cols = row.find_elements(By.TAG_NAME, "tr")
        for col in cols:
            cities.append(col.text)
    return cities

#row_table retorna as cidades da primeira página de municípios.
def row_table(driver):
    tb='/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table[2]' #xpath da tabela alvo.
    table_id = driver.find_element(By.XPATH, tb)
    rows = table_id.find_elements(By.TAG_NAME, "tbody") #pega todas as linhas da tabela.
    cities = []  #armazena as cidades e ceps encontrados.
    for row in rows:
        #pega todas as colunas da tabela alvo.
        cols = row.find_elements(By.TAG_NAME, "tr")
        for col in cols:
            cities.append(col.text)
    return cities

#read_uf busca os estados e no elemento de seleção e clica no botão de busca.
def read_uf(driver, uf):
    find_uf = driver.find_element_by_name('UF')
    select = Select(find_uf)
    select.select_by_visible_text('')
    select.select_by_value(uf)
    btn = driver.find_element_by_xpath('//*[@id="Geral"]/div/div/div[4]/input')
    btn.click()
    time.sleep(1) #intervalo de 1 segundo.


if __name__ == "__main__":
    #Inicia opções do driver do firefox.
    opts = webdriver.FirefoxOptions() 
    opts.add_argument('--headless') #oculta a exibição do navegador.
    driver = webdriver.Firefox(options=opts) #inicia o driver com as opções.
    
    #url da página alvo.
    url='https://www2.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm'
    driver.get(url) #executa o driver na página alvo.
    element = driver.find_elements_by_xpath('//*[@id="Geral"]/div/div/span[2]/label/select') #busca o objeto select que possui os estados(UFs).
    
    #Após encontrar todas as UFs que devem ser buscadas a lógica principal
    #irá selecionar cada estado e percorrer a página de municípios e intervalos de CEPs existentes
    #por estado. Ao final desta busca irá armazenar, cidade, e o intervalo de CEPs.
    uf = ""
    for e in element:
        uf = e.text
        break
    UFs = uf.split('\n')[0:]
    cities_uf = {} #armazena os registros.
    for uf in UFs:
        print("Starting UF", uf)
        read_uf(driver, uf)
        clk = 1
        cities_uf[uf] = []
        try:
            print("Page ", clk, uf)
            cities = row_table(driver) #Faz a primeira busca na página do estado.
            cities_uf[uf] = cities
            #Caso exista uma próxima página de municípios e CEPs a lógica irá entrar na próxima página e armazenar os dados
            #caso contrário irá para o próximo estado.
            while 1:
                lk = '/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/a' #XPATH da próxima página de um estado.
                btn = driver.find_element_by_xpath(lk) 
                btn.click()
                
                #Busca na próxima página os dados de municípios e CEPs.
                cities = next_table(driver)
                if cities not in cities_uf[uf]:
                    clk+=1
                    cities_uf[uf] = cities_uf[uf] + cities
                    print("Page ", clk, uf)
                else:
                    print("Page", clk, uf, 'exists, now exiting.')
                    break;
                time.sleep(1)
        except Exception as e:
            print("Finishing UF", uf)
            print('')
            time.sleep(1)
            driver.get(url) #reincia a busca para o próximo estado da lista de UFs.
    
    #Salva os dados do dicionário para continuar deste ponto caso seja necessário
    a_file = open("dict_data.json", "w")
    json.dump(cities_uf, a_file)
    a_file.close()
    
    #Este trecho carrega os dados do dicionário salvo
    # a_file = open("dict_data.json", "r")
    # cities_uf = json.load(a_file)
    # a_file.close()

    print("Processing UFs data, CEP and cities.")
    #O objetivo é tranformar os dados de acordo com o seguinte padrão de saída JSONL como exemplo:
    #{'id': '109705-67', 'localidade': 'ACRELÂNDIA', 'faixa_de_cep': ['69945-000', '69949-999']}
    #Esta função processa os dados para obter o arquivo result.jsonl com os dados no formato esperado.
    process_data.process_cep_data(cities_uf)
    print("Finish result.jsonl was created.")
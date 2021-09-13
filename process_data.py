#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import numpy as np

#Usando um random para inserir um dígito DV ao final do código
#com o valor 1 o random poderá ser reproduzido sempre que usado
#com este código
np.random.seed(1)

#Esta função cria um código usando os 4 primeiros dígitos do hash calculado
#pelo nome do município em seguida adiciona um dígito aleatório para o código
#hash. O intuito é criar um código diferente para cada ocorrência de municípios
#mesmo que o município tenha 2 ou mais listas de faixa de ceps isto irá diferenciá-las
#por fim é adicionado um código do estado apenas para criar uma faixa de dígitos
#que pode agrupar os código por estado.
def gen_code(uf, city):
    code = uf+city
    hash_object = hashlib.sha1(code.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    val = str(hex_dig)[:4]
    val = int(val, 16)
    dig1 = np.random.randint(0, 10)
    dig2 = ord(uf[0])+ord(uf[1])
    return str(val)+str(dig1)+'-'+str(dig2-65)

#Existem 2 padrões de dados recuperados
#Padrão 1
#Nova Olinda do Norte 69230-000 a 69239-999 Não codificada
#Padrão 2
#Feira de Santana 44000-001 a 44149-999 Codificado
#O objetivo aqui é extrair os dados do padrão 1 e 2 e colocá-los no padrão a seguir:
#{'id': '716234-34', 'localidade': 'FEIRA DE SANTANA', 'faixa_de_cep': ['44000-001', '44149-999']}
#{'id': '234192-65', 'localidade': 'NOVA OLINDA DO NORTE', 'faixa_de_cep': ['69230-000','69239-999']}
#Esta função processa os dados e no final cria um arquivo chamado result.jsonl
def process_cep_data(cities_uf):
    fl = open('result.jsonl', 'w')
    clean_cities_uf = []
    #Processando as cidade por estados
    for uf in cities_uf.keys():
        for cities in cities_uf[uf]:
            if 'Não codificada' in cities:
                line = cities.split('Não codificada')[0]
                line = line.split()
                city = ' '.join(line[:-3]).upper()
                range_cep = [line[-3], line[-1]]
                res_id = gen_code(uf, city)
                result = {'id':res_id, 'localidade':city, 'faixa_de_cep':range_cep}
                clean_cities_uf.append(result)
                fl.write(str(result)+'\n')
            elif 'Codificado' in cities:
                line = cities.split('Codificado')[0]
                #Feira de Santana 44000-001 a 44149-999
                #[Feira, de, Santana, 44000-001, a, 44149-999]
                line = line.split()
                city = ' '.join(line[:-3]).upper()
                range_cep = [line[-3], line[-1]]
                res_id = gen_code(uf, city)
                result = {'id':res_id, 'localidade':city, 'faixa_de_cep':range_cep}
                clean_cities_uf.append(result)
                fl.write(str(result)+'\n')
    fl.close()

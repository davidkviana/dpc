### Data Pirates challenge

#### Objetivo:

Este projeto tem objetivo de criar de forma automática um dataset com todos os municípios brasileiros e suas faixas de CEPs.


#### Metodologia:

Foi utilizado site dos correios na seguite url, https://www2.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm, que pode fornecer todos os municípios e suas faixas de CEPs de acordo com o Estado da Federação pesquisado.

Neste caso utilizou-se todas as UFs possíveis de acordo com o campo UF do site: 'AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP' e 'TO'. 
A partir destes estados buscou-se todas as cidades com suas respectivas faixas de CEPs.

A linguagem de programação utilizada foi python3.8 juntamente com as seguintes bibliotecas que necessitam de instalação, selenium e pandas.


#### Resultados:

Como resultado foram gerados 2 arquivos, um arquivo intermediário ('dict_data.json') e um final ('result.jsonl').

O arquivo 'dict_data.json', é um dicionário contendo os dados brutos, com todos os registros buscados em formato json que pode ser usado para evitar realizar toda a busca no site novamente.

Como pedido no desafio, o arquivo final 'result.jsonl', contém os dados processados e está no formato JSONL. Cada linha do arquivo possui o seguinte formato json como padrão:

{'id': '109705-67', 'localidade': 'ACRELÂNDIA', 'faixa_de_cep': ['69945-000', '69949-999']}

{'id': '30918-67', 'localidade': 'ASSIS BRASIL', 'faixa_de_cep': ['69935-000', '69939-999']}

#### Arquivos python:

O projeto possui 3 arquivos: main.py, process_data.py e test.py.
O arquivo main.py é o arquivo principal do projeto e nele está contido a lógica que realiza as buscas por cada cidade de um estado selecionado.
O arquivo process_data.py é um arquivo secundário que faz o processamento dos dados brutos para tranformar os registros nas saídas já mencionadas:

{'id': '109705-67', 'localidade': 'ACRELÂNDIA', 'faixa_de_cep': ['69945-000', '69949-999']}

{'id': '30918-67', 'localidade': 'ASSIS BRASIL', 'faixa_de_cep': ['69935-000', '69939-999']}

Caso haja necessidade de entender o passo a passo da lógica desenvolvida, ambos os arquivos foram comentados para esta finalidade, contudo, não foi feito docstring dos mesmos pois o objetivo desta apresentação não foi de documentar as funções criadas e sim explicar o que estão realizando de forma mais expositiva.

O arquivo test.py realiza alguns testes para verificar se o banco possui o número de linhas superior ao número de municípios, 5.568, mas limitado ao valor testado até então, 5.673, pois existem municípios que podem possuir mais de uma faixa de CEPs.


#### Execução:

Assumindo que o usuário já possui o python3.8 instalado e o selenium, o json é uma biblioteca que já está inclusa por padrão no python, então, o usuário pode executar o comando:
python3.8 main.py

Logo em seguida pode acompanhar a saída do programa:

![inicio.png <](https://github.com/davidkviana/dpc/blob/master/inicio.png)

![fim.png <](https://github.com/davidkviana/dpc/blob/master/fim.png)



Ao finalizar pode ser verificado a criação dos 2 arquivos: 'dict_data.json' e 'result.jsonl'

![results.png <](https://github.com/davidkviana/dpc/blob/master/results.png)

#### Testes:

Assumindo que o usuário já possui a biblioteca pandas instalada.
Para executar os testes o usuário pode executar o seguinte comando: 
python3.8 test.py

Para verificar o dataset criado deve-se levar em conta que o Brasil possui 5.568 municípios, e de acordo com o o padrão usado no JSON deve haver 3 colunas no dataset. Então foi criado um script de testes para validar as seguintes condições:


1. Existem valores de 'id' duplicados no dataset?
2. O número de colunas corresponde a 3 e são 'id', 'localidade' e 'faixa_de_cep'?
3. O número de registros está entre 5.568 e 5.673?


Foi levado em consideração que o dataset pode ter em alguns municípios mais de uma faixa de CEPs. Assim, é oportuno aceitar até 5.573 municipios pois as rodadas de execução testadas não foram superior a este valor, pois, mas superior ao número de municípios, como mencionado alguns muncípios têm mais de uma faixa diferente de CEPs, logo, também em caso de um número menor que o total de municípios, 5.568, ou maior que 5.573, deve ser verificado o dataset gerado e se houve alguma mudança nos scripts até então criados.

Os resultados serão válidos quando todas as mensagens apresentam 'ok' no final. Caso apresente algum 'fail'. Precisa ser executado main.py novamente e o dataset ser também verificado em caso de erros não listados neste teste.

Exemplo de resultados ok.

![test.png <](https://github.com/davidkviana/dpc/blob/master/test.png)



# Estudo de Machine Learning: Dados de Pesca do Robalo

Este repositório contém um conjunto de dados de pesca do robalo, utilizados para um estudo de machine learning. Os dados são armazenados em um banco de dados **PostgreSQL** local, com o objetivo de realizar análise preditiva sobre as condições ambientais e a quantidade de robalos pescados. O script fornecido neste repositório permite inserir ou atualizar esses dados no banco PostgreSQL com base em um arquivo CSV.

## Estrutura do Projeto

- **insert.py**: Script Python responsável por importar os dados de pesca (de um arquivo CSV) para o banco de dados PostgreSQL local. O script inclui funcionalidade para **evitar duplicação** de dados e **atualizar** registros existentes.
- **dados_pesca.csv**: Arquivo CSV contendo os dados de pesca, com as colunas necessárias para o estudo.

## Pré-requisitos

Antes de rodar o script Python, é necessário configurar o ambiente de desenvolvimento. Para isso, siga os passos abaixo:

### 1. Instalar o PostgreSQL

O PostgreSQL deve estar instalado localmente para executar o script. Caso ainda não tenha o PostgreSQL, você pode instalá-lo a partir de [aqui](https://www.postgresql.org/download/).

### 2. Criar o Banco de Dados

Após instalar o PostgreSQL, crie um banco de dados local chamado `postgres` (ou outro nome de sua escolha). Para isso, execute os seguintes comandos no terminal:

```bash
psql -U postgres
CREATE DATABASE postgres;
```

### 3. Configurar a Tabela no PostgreSQL
O script insert.py insere os dados de pesca na tabela dados_pesca. Antes de executar o script, crie a tabela no seu banco PostgreSQL com a seguinte estrutura:

```bash
CREATE TABLE dados_pesca (
    data DATE,
    temperatura_agua FLOAT,
    oxigenio_dissolvido FLOAT,
    estacao_ano VARCHAR(20),
    fase_lua VARCHAR(20),
    clima VARCHAR(20),
    hora_dia VARCHAR(20),
    tipo_peixe VARCHAR(20),
    quantidade INT,
    localizacao VARCHAR(255),
    PRIMARY KEY (data, localizacao)  -- Definição de chave primária
);
```
### 4. Adicionar a Restrição de Unicidade
Para evitar a inserção de dados duplicados, adicione a chave única para os campos data e localizacao:

```bash
ALTER TABLE dados_pesca
ADD CONSTRAINT unique_data_localizacao UNIQUE (data, localizacao);
```


# Executando o Script

Após configurar o banco de dados, execute o script `insert.py` para inserir ou atualizar os dados no banco PostgreSQL:

```bash
python insert.py
```

O script lê o arquivo CSV `dados_pesca.csv`, processa os dados e insere ou atualiza os registros na tabela `dados_pesca` do banco de dados PostgreSQL.

## Estrutura do CSV

O arquivo CSV `dados_pesca.csv` deve conter as seguintes colunas:

- `data`: Data da pesca (formato: YYYY-MM-DD)
- `temperatura_agua`: Temperatura da água (em graus Celsius)
- `oxigenio_dissolvido`: Nível de oxigênio dissolvido na água (em mg/L)
- `estacao_ano`: Estação do ano (ex.: Verão, Outono, etc.)
- `fase_lua`: Fase da lua (ex.: Lua Crescente, Lua Cheia, etc.)
- `clima`: Condição climática no momento da pesca (ex.: Nublado, Ensolarado, etc.)
- `hora_dia`: Hora do dia (ex.: Manhã, Tarde, Noite)
- `tipo_peixe`: Tipo de peixe pescado (ex.: Robalo)
- `quantidade`: Quantidade de peixe pescado
- `localizacao`: Localização da pesca (pode ser coordenadas geográficas ou um nome de local, como "Mureta,Santos")

### Exemplo de conteúdo do arquivo CSV:

```bash
data,temperatura_agua,oxigenio_dissolvido,estacao_ano,fase_lua,clima,hora_dia,tipo_peixe,quantidade,localizacao
2025-01-08,24.1,6.9,Verão,Lua Crescente,Nublado,Manha,Robalo,3,"-23.5713,-46.6396"
2025-01-14,26.5,5.2,Primavera,Lua Minguante,Ventoso,Tarde,Robalo,1,"-23.5305,-46.6652"
```

## Como Funciona

O script `insert.py` lê o arquivo CSV e insere os dados na tabela `dados_pesca` do banco de dados PostgreSQL.

Se os dados já existirem no banco para uma combinação de `data` e `localizacao`, o script atualiza os dados existentes.

Caso contrário, ele insere os dados como novos registros.

## Projeto ainda em construção

## Contribuições

Se você deseja contribuir com este projeto, fique à vontade para fazer um fork e enviar um pull request com suas modificações.


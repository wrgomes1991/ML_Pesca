import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

import psycopg2
import numpy as np

# Função para calcular a estação do ano com base no mês
def calcular_estacao_ano(mes):
    if mes in [12, 1, 2]:
        return 'Verão'
    elif mes in [3, 4, 5]:
        return 'Outono'
    elif mes in [6, 7, 8]:
        return 'Inverno'
    else:
        return 'Primavera'

# Função simplificada para calcular a fase da lua
def calcular_fase_lua(data):
    # Aproximação simplificada com base na data
    base_data = datetime(2025, 1, 1)  # Lua cheia em 2025-01-01
    diff = (data - base_data).days
    fase = diff % 29  # Ciclo lunar de aproximadamente 29,5 dias

    if fase < 7:
        return 'Lua Crescente'
    elif fase < 14:
        return 'Lua Cheia'
    elif fase < 22:
        return 'Lua Minguante'
    else:
        return 'Lua Nova'

# Configuração de conexão com o PostgreSQL
conn = psycopg2.connect(
    host="localhost",         # Substitua pelo seu host PostgreSQL
    user="robalo_app",        # Substitua pelo seu usuário PostgreSQL
    password="reidomangue",   # Substitua pela sua senha PostgreSQL
    database="postgres"       # Substitua pelo nome do seu banco de dados
)

# Criar um cursor
cursor = conn.cursor()

# Consulta SQL para selecionar todos os dados da tabela 'dados_pesca'
sql = "SELECT * FROM dados_pesca"

# Executando a consulta
cursor.execute(sql)

# Recuperando os dados
rows = cursor.fetchall()

# Criando um DataFrame pandas a partir dos dados recuperados
df = pd.DataFrame(rows, columns=[
    'data', 'temperatura_agua', 'oxigenio_dissolvido', 'estacao_ano', 'fase_lua', 
    'clima', 'hora_dia', 'tipo_peixe', 'quantidade', 'localizacao'
])

# Fechar a conexão e o cursor
cursor.close()
conn.close()

# Exibir os dados
print(df)

# Criando a coluna alvo: 1 se a quantidade for maior que 4, caso contrário 0
df['deve_ir_pescar'] = df['quantidade'].apply(lambda x: 1 if x > 4 else 0)

# Convertendo a coluna de data para o tipo datetime
df['data'] = pd.to_datetime(df['data'])

# Calculando a diferença em dias a partir de uma data fixa (hoje, por exemplo)
hoje = datetime.now()
df['dias_para_data'] = (hoje - df['data']).dt.days

# Codificando variáveis categóricas usando LabelEncoder
le_estacao = LabelEncoder()
le_fase_lua = LabelEncoder()
le_clima = LabelEncoder()
le_hora_dia = LabelEncoder()

# Fit em todos os dados conhecidos
df['estacao_ano'] = le_estacao.fit_transform(df['estacao_ano'])
df['fase_lua'] = le_fase_lua.fit_transform(df['fase_lua'])
df['clima'] = le_clima.fit_transform(df['clima'])
df['hora_dia'] = le_hora_dia.fit_transform(df['hora_dia'])

# Função para lidar com rótulos desconhecidos
def transform_with_default(encoder, value, default_value=-1):
    """Transforma valor, retornando o índice do valor ou o valor padrão se desconhecido."""
    try:
        return encoder.transform([value])[0]
    except ValueError:  # Quando o valor não for encontrado no encoder
        return default_value

# Solicitar a data desejada de pesca do usuário
data_pesca_str = input("Digite a data que deseja ir pescar (formato: YYYY-MM-DD): ")

# Converter a data fornecida em string para datetime
try:
    data_pesca = datetime.strptime(data_pesca_str, "%Y-%m-%d")
except ValueError:
    print("Formato de data inválido. Usando a data atual.")
    data_pesca = hoje  # Caso o formato seja inválido, usar a data atual

# Calcular a diferença em dias entre a data fornecida e a data de hoje
dias_para_data_input = (data_pesca - hoje).days

# Calcular a estação do ano e a fase da lua para a data fornecida
estacao_ano_input = calcular_estacao_ano(data_pesca.month)
fase_lua_input = calcular_fase_lua(data_pesca)

# Solicitar o clima para o dia de pesca
clima_input = input("Digite o clima para o dia desejado (Exemplo: Ensolarado, Nublado, Chuvoso): ")

# Criando nova entrada de dados com a data fornecida
nova_data = {
    'temperatura_agua': [23.0],
    'oxigenio_dissolvido': [6.5],
    'estacao_ano': [transform_with_default(le_estacao, estacao_ano_input)],
    'fase_lua': [transform_with_default(le_fase_lua, fase_lua_input)],
    'clima': [transform_with_default(le_clima, clima_input)],
    'hora_dia': [transform_with_default(le_hora_dia, 'Tarde')],  # Assumindo 'Tarde' como input
    'dias_para_data': [dias_para_data_input]  # Usando a diferença em dias calculada
}

nova_df = pd.DataFrame(nova_data)

# Definir as variáveis independentes (X) e a variável dependente (y)
X = df[['temperatura_agua', 'oxigenio_dissolvido', 'estacao_ano', 'fase_lua', 'clima', 'hora_dia', 'dias_para_data']]
y = df['deve_ir_pescar']

# Dividir os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar e treinar o modelo de Árvore de Decisão
modelo = DecisionTreeClassifier(random_state=42)
modelo.fit(X_train, y_train)

# Fazer previsões
y_pred = modelo.predict(X_test)


# Prever se deve ou não pescar
predicao = modelo.predict(nova_df)

# Obter a árvore de decisão para verificar as variáveis mais importantes
feature_names = ['temperatura_agua', 'oxigenio_dissolvido', 'estacao_ano', 'fase_lua', 'clima', 'hora_dia', 'dias_para_data']
importancia = modelo.feature_importances_


# Imprimir explicação sobre a previsão
if predicao[0] == 1:
    print(f"Deve ir pescar porque o histórico mostra que a fase lunar {fase_lua_input} na estação {estacao_ano_input} teve bons resultados no passado!")
else:
    print(f"Não deve ir pescar porque o histórico mostra que a fase lunar {fase_lua_input} na estação {estacao_ano_input} teve resultados baixos no passado.")

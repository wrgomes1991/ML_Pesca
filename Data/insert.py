import psycopg2
import csv

# Configuração da conexão com o PostgreSQL usando psycopg2
conn = psycopg2.connect(
    host="localhost",         
    user="robalo_app",            
    password="reidomangue",   
    database="postgres"       
)

cursor = conn.cursor()

# Caminho para o arquivo CSV
csv_file_path = 'ML_Pesca/Data/dados_pesca.csv'

# SQL para inserção ou atualização dos dados
sql = """
INSERT INTO dados_pesca 
(data, temperatura_agua, oxigenio_dissolvido, estacao_ano, fase_lua, clima, hora_dia, tipo_peixe, quantidade, localizacao)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (data, localizacao) 
DO UPDATE SET 
temperatura_agua = EXCLUDED.temperatura_agua,
oxigenio_dissolvido = EXCLUDED.oxigenio_dissolvido,
estacao_ano = EXCLUDED.estacao_ano,
fase_lua = EXCLUDED.fase_lua,
clima = EXCLUDED.clima,
hora_dia = EXCLUDED.hora_dia,
tipo_peixe = EXCLUDED.tipo_peixe,
quantidade = EXCLUDED.quantidade;
"""

# Lendo o arquivo CSV com a codificação 'ISO-8859-1' ou 'latin1'
with open(csv_file_path, newline='', encoding='ISO-8859-1') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Pula o cabeçalho

    # Inserindo ou atualizando os dados no banco de dados
    for row in csvreader:
        # Verificar se a linha possui o número adequado de colunas
        if len(row) >= 10:  # Verifica se há pelo menos 10 colunas
            data = {
                'data': row[0],
                'temperatura_agua': float(row[1]),
                'oxigenio_dissolvido': float(row[2]),
                'estacao_ano': row[3],
                'fase_lua': row[4],
                'clima': row[5],
                'hora_dia': row[6],
                'tipo_peixe': row[7],
                'quantidade': int(row[8]),
                # Garantir que a 'localizacao' tenha o formato correto
                'localizacao': row[9] if len(row) > 9 else None
            }

            # Verificar se localizacao foi atribuída corretamente
            if data['localizacao'] is None:
                print(f"Atenção: Localização ausente ou mal formatada para a data: {data['data']}")

            # Inserir ou atualizar os dados no banco
            cursor.execute(sql, (data['data'], data['temperatura_agua'], data['oxigenio_dissolvido'], data['estacao_ano'], 
                                 data['fase_lua'], data['clima'], data['hora_dia'], data['tipo_peixe'], 
                                 data['quantidade'], data['localizacao']))
        else:
            print(f"Erro na linha: {row}, quantidade insuficiente de colunas.")

# Confirmando a transação
conn.commit()

# Fechando a conexão
cursor.close()
conn.close()

print("Dados inseridos ou atualizados com sucesso!")

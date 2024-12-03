import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# Configurar o backend para "Agg", adequado para ambientes não interativos
matplotlib.use('Agg')

# Defina os arquivos CSV para cada número de usuários
files = {
    "10-REST": "10-REST.csv",
    "100-REST": "100-REST.csv",
    "1000-REST": "1000-REST.csv",
    "10-GraphQL": "10-Graphql.csv",
    "100-GraphQL": "100-Graphql.csv",
    "1000-GraphQL": "1000-Graphql.csv",
    "10-SOAP": "10-SOAP.csv",
    "100-SOAP": "100-SOAP.csv",
    "1000-SOAP": "1000-SOAP.csv"
}

# Filtrando as requisições REST, GraphQL e SOAP
rest_queries = [
    "GET /usuarios",
    "GET /musicas",
    "GET /usuarios/1/playlists",
    "GET /playlists/1",
    "GET /musicas/1/playlists"
]

graphql_queries = [
    "GraphQL: Musica",
    "GraphQL: Musicas",
    "GraphQL: Playlist",
    "GraphQL: PlaylistsPorUsuario",
    "GraphQL: Usuarios"
]

soap_queries = [
    "SOAP - listarMusicas",
    "SOAP - listarUsuarios"
]

# Dicionário para armazenar os tempos médios de resposta
response_times = {
    "REST": {},
    "GraphQL": {},
    "SOAP": {}
}

# Função para calcular o tempo médio de resposta
def calculate_avg_response_time(df, queries):
    filtered_data = df[df['Name'].isin(queries)]
    return filtered_data['Average Response Time'].mean()

# Processar cada arquivo CSV
for file_name, file_path in files.items():
    df = pd.read_csv(file_path)
    
    # Verificar se o arquivo é REST, GraphQL ou SOAP
    if "REST" in file_name:
        key = "REST"
        queries = rest_queries
    elif "GraphQL" in file_name:
        key = "GraphQL"
        queries = graphql_queries
    else:
        key = "SOAP"
        queries = soap_queries
        print(f"Processando {file_name}")
        print("Consultas encontradas no CSV:", df['Name'].unique())  # Debugging
    
    user_count = file_name.split('-')[0]
    
    # Calcular o tempo médio de resposta para as requisições
    avg_response_time = calculate_avg_response_time(df, queries)
    
    # Garantir que valores inválidos não causem problemas
    if pd.isna(avg_response_time):
        avg_response_time = 0  # Substitua por um valor padrão adequado, se necessário
    
    # Armazenar o resultado no dicionário
    if user_count not in response_times[key]:
        response_times[key][user_count] = []
    
    response_times[key][user_count].append(avg_response_time)

# Preparar os dados para o gráfico
rest_avg_times = [response_times["REST"][str(num)][0] for num in [10, 100, 1000]]
graphql_avg_times = [response_times["GraphQL"][str(num)][0] for num in [10, 100, 1000]]
soap_avg_times = [response_times["SOAP"][str(num)][0] for num in [10, 100, 1000]]

# Verificar os valores calculados
print("Tempos Médios Calculados:")
print(f"REST: {rest_avg_times}")
print(f"GraphQL: {graphql_avg_times}")
print(f"SOAP: {soap_avg_times}")

# Configurar o gráfico
bar_width = 0.25
x = range(len([10, 100, 1000]))  # Número de usuários

# Plotar os dados
plt.bar(x, rest_avg_times, bar_width, label="REST", color='blue')
plt.bar([i + bar_width for i in x], graphql_avg_times, bar_width, label="GraphQL", color='green')
plt.bar([i + 2 * bar_width for i in x], soap_avg_times, bar_width, label="SOAP", color='orange')

# Ajustar as posições no eixo X
plt.xticks([i + bar_width for i in x], ['10', '100', '1000'])

# Adicionar título e legendas
plt.title('Comparação de Tempo de Resposta Médio entre REST, GraphQL e SOAP')
plt.xlabel('Número de Usuários')
plt.ylabel('Tempo Médio de Resposta (ms)')
plt.legend()

# Salvar o gráfico
plt.savefig("grafico_comparacao.png")
print("O gráfico foi salvo como 'grafico_comparacao.png'.")

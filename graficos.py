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
    "1000-GraphQL": "1000-Graphql.csv"
}

# Filtrando as requisições REST e GraphQL
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

# Dicionário para armazenar os tempos médios de resposta
response_times = {
    "REST": {},
    "GraphQL": {}
}

# Função para calcular o tempo médio de resposta
def calculate_avg_response_time(df, queries):
    filtered_data = df[df['Name'].isin(queries)]
    return filtered_data['Average Response Time'].mean()

# Processar cada arquivo CSV
for file_name, file_path in files.items():
    df = pd.read_csv(file_path)
    
    # Verificar se o arquivo é REST ou GraphQL
    if "REST" in file_name:
        key = "REST"
    else:
        key = "GraphQL"
    
    user_count = file_name.split('-')[0]
    
    # Calcular o tempo médio de resposta para as requisições
    avg_response_time = calculate_avg_response_time(df, rest_queries if key == "REST" else graphql_queries)
    
    # Armazenar o resultado no dicionário
    if user_count not in response_times[key]:
        response_times[key][user_count] = []
    
    response_times[key][user_count].append(avg_response_time)

# Preparar os dados para o gráfico
rest_avg_times = [response_times["REST"][str(num)][0] for num in [10, 100, 1000]]
graphql_avg_times = [response_times["GraphQL"][str(num)][0] for num in [10, 100, 1000]]

# Configurar o gráfico
bar_width = 0.35
x = range(len([10, 100, 1000]))  # Número de usuários

# Plotar os dados
plt.bar(x, rest_avg_times, bar_width, label="REST", color='blue')
plt.bar([i + bar_width for i in x], graphql_avg_times, bar_width, label="GraphQL", color='green')

# Adicionar título e labels
plt.title('Comparação de Tempo de Resposta Médio entre REST e GraphQL')
plt.xlabel('Número de Usuários')
plt.ylabel('Tempo Médio de Resposta (ms)')
plt.xticks([i + bar_width / 2 for i in x], ['10', '100', '1000'])
plt.legend()

# Salvar o gráfico em um arquivo PNG
plt.savefig("grafico_comparacao.png")

# Exibir uma mensagem indicando que o gráfico foi salvo
print("O gráfico foi salvo como 'grafico_comparacao.png'.")

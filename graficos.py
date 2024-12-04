import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

files = {
    "10-REST": "10-REST.csv",
    "100-REST": "100-REST.csv",
    "1000-REST": "1000-REST.csv",
    "10-GraphQL": "10-Graphql.csv",
    "100-GraphQL": "100-Graphql.csv",
    "1000-GraphQL": "1000-Graphql.csv",
    "10-SOAP": "10-SOAP.csv",
    "100-SOAP": "100-SOAP.csv",
    "1000-SOAP": "1000-SOAP.csv",
    "10-gRPC": "10-gRPC.csv",
    "100-gRPC": "100-gRPC.csv",  
    "1000-gRPC": "1000-gRPC.csv" 
}

# Consultas para REST, GraphQL, SOAP e gRPC
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

grpc_queries = [
    "gRPC: ListUsers",
    "gRPC: ListSongs",
    "gRPC: ListPlaylistsByUser",
    "gRPC: ListSongsByPlaylist",
    "gRPC: ListPlaylistsBySong"
]

# Dicionário para armazenar os tempos médios de resposta
response_times = {
    "REST": {},
    "GraphQL": {},
    "SOAP": {},
    "gRPC": {}  
}

# Função para calcular o tempo médio de resposta
def calculate_avg_response_time(df, queries):
    filtered_data = df[df['Name'].isin(queries)]
    return filtered_data['Average Response Time'].mean()

def calculate_avg_response_time_grpc(df, queries):
    filtered_data = df[df['Name'].isin(queries)]
    return filtered_data['Average Response Time'].mean()

# Processar cada arquivo CSV
for file_name, file_path in files.items():
    df = pd.read_csv(file_path)
    
    # Verificar se o arquivo é REST, GraphQL, SOAP ou gRPC
    if "REST" in file_name:
        key = "REST"
        queries = rest_queries
    elif "GraphQL" in file_name:
        key = "GraphQL"
        queries = graphql_queries
    elif "SOAP" in file_name:
        key = "SOAP"
        queries = soap_queries
    elif "gRPC" in file_name: 
        key = "gRPC"
        queries = grpc_queries
    else:
        continue  
    
    user_count = file_name.split('-')[0]
    
    # Calcular o tempo médio de resposta para as requisições
    if key == "gRPC":
        avg_response_time = calculate_avg_response_time_grpc(df, queries)
    else:
        avg_response_time = calculate_avg_response_time(df, queries)
    
    if pd.isna(avg_response_time):
        avg_response_time = 0  

    if user_count not in response_times[key]:
        response_times[key][user_count] = []
    
    response_times[key][user_count].append(avg_response_time)

rest_avg_times = [response_times["REST"][str(num)][0] for num in [10, 100, 1000]]
graphql_avg_times = [response_times["GraphQL"][str(num)][0] for num in [10, 100, 1000]]
soap_avg_times = [response_times["SOAP"][str(num)][0] for num in [10, 100, 1000]]
grpc_avg_times = [response_times["gRPC"][str(num)][0] for num in [10, 100, 1000]]

print("Tempos Médios Calculados:")
print(f"REST: {rest_avg_times}")
print(f"GraphQL: {graphql_avg_times}")
print(f"SOAP: {soap_avg_times}")
print(f"gRPC: {grpc_avg_times}")

bar_width = 0.2  # Reduzido para ajustar o número de barras
x = range(len([10, 100, 1000]))  # Número de usuários

# Plotar os dados
plt.bar(x, rest_avg_times, bar_width, label="REST", color='blue')
plt.bar([i + bar_width for i in x], graphql_avg_times, bar_width, label="GraphQL", color='green')
plt.bar([i + 2 * bar_width for i in x], soap_avg_times, bar_width, label="SOAP", color='orange')
plt.bar([i + 3 * bar_width for i in x], grpc_avg_times, bar_width, label="gRPC", color='red') 

# Ajustar as posições no eixo X
plt.xticks([i + 1.5 * bar_width for i in x], ['10', '100', '1000'])

plt.title('Comparação de Tempo de Resposta Médio entre REST, GraphQL, SOAP e gRPC')
plt.xlabel('Número de Usuários')
plt.ylabel('Tempo Médio de Resposta (ms)')
plt.legend()

# Salvar o gráfico
plt.savefig("grafico_comparacao.png")
print("O gráfico foi salvo como grafico_comparacao.png")

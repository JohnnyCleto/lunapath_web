import networkx as nx
import random
import heapq
from math import sqrt

LOCAIS = {
    "Casa de Luna": (10, 10),
    "Estação de Drones": (40, 20),
    "Auditoria Principal": (70, 10),
    "Estação IoT": (20, 50),
    "Cafeteria Tech": (60, 40),
    "Central de Energia": (80, 20),
    "Hospital Futuro": (90, 60),
    "Escola Smart": (40, 90),
    "Museu Digital": (60, 110),
    "Estúdio Holográfico": (80, 110),
    "Praça do Conhecimento": (10, 110),
    "Biblioteca AR": (20, 130),
    "Centro de Robótica": (70, 130),
    "Galeria Virtual": (90, 130),
    "Laboratório Quântico": (100, 40),
    "Centro de Inovação": (100, 80),
    "Mercado Automatizado": (60, 150),
    "Estação Solar": (90, 10),
    "Zoológico Digital": (110, 60),
    "Residência Cyborg": (100, 130),
    "Teatro de Realidade Mista": (110, 150),
    "Parque Inteligente": (10, 30),
    "Clínica de Nanomedicina": (80, 70),
    "Delegacia Neural": (20, 20),
    "Terminal de Ônibus Autônomo": (70, 90),
    "Garagem de Veículos AI": (40, 40),
    "Torre de Comunicação 5G": (10, 130),
    "Observatório de Dados": (90, 150),
    "Laboratório Genético": (60, 20),
    "Academia VR": (110, 20),
    "Centro Financeiro Blockchain": (20, 110),
    "Cinema Imersivo": (100, 10),
    "Ponto de Recarga Elétrica": (40, 130),
    "Estufa Inteligente": (70, 150),
    "Fábrica Automatizada": (80, 130),
    "Base de Drones": (60, 60),
    "Túnel Subterrâneo A": (90, 40),
    "Túnel Subterrâneo B": (100, 70),
    "Ponte Holográfica": (110, 90),
    "Plataforma de Lançamento Espacial": (130, 110),
    "Núcleo de IA": (130, 20),
    "Centro de Transporte Magnético": (120, 60),
    "Estação de Reciclagem Avançada": (130, 40),
    "Parque Eólico Inteligente": (140, 80),
}

# Conexões - lista de tuplas (origem, destino)
# Definiremos conexões realistas entre os pontos para o grafo (bidirecional)
CONEXOES = [
    ("Casa de Luna", "Delegacia Neural"),
    ("Casa de Luna", "Parque Inteligente"),
    ("Delegacia Neural", "Estação de Drones"),
    ("Estação de Drones", "Garagem de Veículos AI"),
    ("Garagem de Veículos AI", "Laboratório Genético"),
    ("Laboratório Genético", "Auditoria Principal"),
    ("Auditoria Principal", "Estação Solar"),
    ("Auditoria Principal", "Central de Energia"),
    ("Central de Energia", "Clínica de Nanomedicina"),
    ("Clínica de Nanomedicina", "Hospital Futuro"),
    ("Hospital Futuro", "Zoológico Digital"),
    ("Hospital Futuro", "Teatro de Realidade Mista"),
    ("Teatro de Realidade Mista", "Parque Eólico Inteligente"),
    ("Parque Eólico Inteligente", "Plataforma de Lançamento Espacial"),
    ("Plataforma de Lançamento Espacial", "Núcleo de IA"),
    ("Núcleo de IA", "Centro de Transporte Magnético"),
    ("Centro de Transporte Magnético", "Estação de Reciclagem Avançada"),
    ("Estação de Reciclagem Avançada", "Parque Eólico Inteligente"),
    ("Parque Inteligente", "Praça do Conhecimento"),
    ("Praça do Conhecimento", "Biblioteca AR"),
    ("Biblioteca AR", "Centro Financeiro Blockchain"),
    ("Centro Financeiro Blockchain", "Escola Smart"),
    ("Escola Smart", "Terminal de Ônibus Autônomo"),
    ("Terminal de Ônibus Autônomo", "Centro de Robótica"),
    ("Centro de Robótica", "Galeria Virtual"),
    ("Galeria Virtual", "Residência Cyborg"),
    ("Residência Cyborg", "Estúdio Holográfico"),
    ("Estúdio Holográfico", "Museu Digital"),
    ("Museu Digital", "Mercado Automatizado"),
    ("Mercado Automatizado", "Estufa Inteligente"),
    ("Estufa Inteligente", "Fábrica Automatizada"),
    ("Fábrica Automatizada", "Base de Drones"),
    ("Base de Drones", "Cafeteria Tech"),
    ("Cafeteria Tech", "Laboratório Quântico"),
    ("Laboratório Quântico", "Centro de Inovação"),
    ("Centro de Inovação", "Cinema Imersivo"),
    ("Cinema Imersivo", "Academia VR"),
    ("Academia VR", "Torre de Comunicação 5G"),
    ("Torre de Comunicação 5G", "Observatório de Dados"),
    ("Observatório de Dados", "Ponto de Recarga Elétrica"),
    ("Ponto de Recarga Elétrica", "Túnel Subterrâneo A"),
    ("Túnel Subterrâneo A", "Túnel Subterrâneo B"),
    ("Túnel Subterrâneo B", "Ponte Holográfica"),
    ("Ponte Holográfica", "Centro de Transporte Magnético"),
    ("Centro de Robótica", "Terminal de Ônibus Autônomo"),
    ("Estação IoT", "Delegacia Neural"),
    ("Estação IoT", "Garagem de Veículos AI"),
]

def distancia_euclidiana(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def gerar_grafo():
    G = nx.Graph()
    # Adiciona nós
    for local, coord in LOCAIS.items():
        G.add_node(local, pos=coord)

    # Adiciona arestas com peso = distância euclidiana
    for u, v in CONEXOES:
        dist = distancia_euclidiana(LOCAIS[u], LOCAIS[v])
        G.add_edge(u, v, weight=dist)

    return G

def dijkstra(grafo, inicio, fim):
    distancias = {n: float("inf") for n in grafo.nodes}
    distancias[inicio] = 0
    anteriores = {n: None for n in grafo.nodes}
    heap = [(0, inicio)]

    while heap:
        dist_atual, no_atual = heapq.heappop(heap)
        if no_atual == fim:
            break
        if dist_atual > distancias[no_atual]:
            continue
        for vizinho in grafo.neighbors(no_atual):
            peso = grafo[no_atual][vizinho]["weight"]
            nova_dist = dist_atual + peso
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                anteriores[vizinho] = no_atual
                heapq.heappush(heap, (nova_dist, vizinho))

    caminho = []
    no = fim
    while no:
        caminho.append(no)
        no = anteriores[no]
    caminho.reverse()

    if distancias[fim] == float("inf"):
        return None, float("inf")
    return caminho, distancias[fim]

# Sensores IoT simulados: congestionamentos por aresta
def atualizar_congestionamento(grafo, intensidade_max=3.0):
    # Intensidade congestionamento multiplicador [1.0 - intensidade_max]
    for u, v in grafo.edges():
        # Chance de congestionamento
        chance = random.random()
        if chance < 0.25:
            # Congestionamento leve a forte
            mult = random.uniform(1.2, intensidade_max)
        else:
            mult = 1.0
        # Peso original
        peso_original = distancia_euclidiana(grafo.nodes[u]['pos'], grafo.nodes[v]['pos'])
        grafo[u][v]['weight'] = peso_original * mult
        grafo[u][v]['congestion'] = mult

def aplicar_imprevistos(grafo):
    # Imprevistos aleatórios que bloqueiam arestas ou aumentam peso
    for u, v in grafo.edges():
        chance = random.random()
        if chance < 0.10:
            # Obra/bloqueio - peso infinito (aresta indisponível)
            grafo[u][v]['weight'] = float('inf')
            grafo[u][v]['blocked'] = True
        elif chance < 0.25:
            # Obra leve ou incidente - peso aumentado
            mult = random.uniform(1.5, 4.0)
            peso_original = distancia_euclidiana(grafo.nodes[u]['pos'], grafo.nodes[v]['pos'])
            grafo[u][v]['weight'] = peso_original * mult
            grafo[u][v]['blocked'] = False
        else:
            if 'blocked' in grafo[u][v]:
                grafo[u][v]['blocked'] = False

def simular_rota(inicio, fim, aplicar_imprevistos_apos_primeira=True):
    grafo = gerar_grafo()
    # Primeiro cálculo sem imprevistos
    atualizar_congestionamento(grafo)
    caminho, custo = dijkstra(grafo, inicio, fim)
    # Se permitido, aplica imprevistos e recalcula
    if aplicar_imprevistos_apos_primeira:
        aplicar_imprevistos(grafo)
        atualizar_congestionamento(grafo)  # Atualiza congestionamento após imprevistos
        caminho_novo, custo_novo = dijkstra(grafo, inicio, fim)
        # Retorna a melhor rota entre as duas (primeira e segunda tentativa)
        if caminho_novo and custo_novo < custo:
            return caminho_novo, custo_novo, True
        else:
            return caminho, custo, False
    else:
        return caminho, custo, False

def obter_posicoes(grafo):
    return {n: data['pos'] for n, data in grafo.nodes(data=True)}

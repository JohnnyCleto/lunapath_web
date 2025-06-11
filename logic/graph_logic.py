import networkx as nx
from math import sqrt

LOCAIS = {
    "Casa de Luna": (0, 0),
    "Estação de Drones": (2, 1),
    "Auditoria Principal": (4, 0),
    "Estação IoT": (1, 3),
    "Cafeteria Tech": (3, 2),
    "Central de Energia": (5, 1),
    "Hospital Futuro": (6, 3),
    "Escola Smart": (2, 4),
    "Museu Digital": (3, 5),
    "Estúdio Holográfico": (5, 5),
    "Praça do Conhecimento": (0, 5),
    "Biblioteca AR": (1, 6),
    "Centro de Robótica": (4, 6),
    "Galeria Virtual": (6, 6),
    "Laboratório Quântico": (7, 2),
    "Centro de Inovação": (7, 4),
    "Mercado Automatizado": (3, 7),
    "Estação Solar": (6, 0),
    "Zoológico Digital": (8, 3),
    "Residência Cyborg": (7, 6),
    "Teatro de Realidade Mista": (8, 5),
    "Parque Inteligente": (0, 2),
    "Clínica de Nanomedicina": (5, 3),
    "Delegacia Neural": (1, 1),
    "Terminal de Ônibus Autônomo": (4, 4),
    "Garagem de Veículos AI": (2, 2),
    "Torre de Comunicação 5G": (0, 6),
    "Observatório de Dados": (6, 7),
    "Laboratório Genético": (3, 1),
    "Academia VR": (8, 1),
    "Centro Financeiro Blockchain": (1, 5),
    "Cinema Imersivo": (7, 1),
    "Ponto de Recarga Elétrica": (2, 6),
    "Estufa Inteligente": (4, 7),
    "Fábrica Automatizada": (5, 6),
    "Base de Drones": (3, 3),
    "Túnel Subterrâneo A": (6, 2),
    "Túnel Subterrâneo B": (0, 3),
    "Ponto de Encontro AR": (2, 0),
    "Posto de Vigilância": (7, 3),
    "Jardim Algorítmico": (6, 5),
    "Escola Infantil Digital": (1, 4),
    "Restaurante Autônomo": (2, 5),
    "Campus AI": (7, 7),
    "Condomínio Verde": (5, 7),
    "Vila Modular": (4, 2),
    "Câmara de Simulação": (3, 4),
    "Núcleo de Energia Limpa": (8, 0),
    "Rooftop Garden": (6, 1),
    "Estação Suborbital": (9, 2),
    "Trilha Sensorial": (8, 6),
}

def distancia(a, b):
    """Calcula a distância Euclidiana entre dois pontos a e b."""
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def gerar_mapa_cidade():
    cidade = nx.Graph()

    # Adiciona todos os locais como nós
    for local, pos in LOCAIS.items():
        cidade.add_node(local, pos=pos)

    # Conectar nós garantindo que cada nó tenha no máximo 3 conexões,
    # priorizando a conexão aos vizinhos mais próximos
    # Também garantir conectividade mínima
    
    # Passo 1: calcular todas as distâncias entre pares de nós
    locais = list(LOCAIS.keys())
    distancias = []
    for i in range(len(locais)):
        for j in range(i+1, len(locais)):
            p1 = LOCAIS[locais[i]]
            p2 = LOCAIS[locais[j]]
            dist = distancia(p1, p2)
            distancias.append((locais[i], locais[j], dist))

    # Ordenar por distância crescente (arestas mais curtas primeiro)
    distancias.sort(key=lambda x: x[2])

    # Para garantir conectividade: vamos primeiro construir uma árvore geradora mínima (MST)
    # Usaremos Kruskal simples: conectar os nós mais próximos, desde que não forme ciclo.
    parent = {}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a,b):
        rootA = find(a)
        rootB = find(b)
        if rootA != rootB:
            parent[rootB] = rootA
            return True
        return False
    
    # Inicializar disjoint set
    for local in locais:
        parent[local] = local

    # Primeiro conectar os nós com MST, sem ultrapassar 3 conexões por nó
    grau = {local: 0 for local in locais}

    for u, v, dist in distancias:
        if grau[u] < 3 and grau[v] < 3 and union(u,v):
            cidade.add_edge(u, v, weight=dist)
            grau[u] += 1
            grau[v] += 1

    # Depois, adicionar arestas extras para nós com menos de 3 conexões, sempre que possível,
    # conectando aos vizinhos mais próximos sem ultrapassar o limite 3 por nó.

    # Função auxiliar para buscar pares possíveis para ligação extra
    def pode_conectar(u, v):
        return (not cidade.has_edge(u, v)) and grau[u] < 3 and grau[v] < 3

    # Tentar adicionar mais arestas para aproximar o limite 3 conexões para cada nó
    for u, v, dist in distancias:
        if pode_conectar(u, v):
            cidade.add_edge(u, v, weight=dist)
            grau[u] += 1
            grau[v] += 1

    return cidade

def dijkstra(grafo, inicio):
    dist = {node: float('inf') for node in grafo.nodes}
    dist[inicio] = 0
    ant = {node: None for node in grafo.nodes}
    visitados = set()
    
    while len(visitados) < len(grafo.nodes):
        # Escolhe o nó não visitado com menor distância
        nao_visitados = {node: dist[node] for node in grafo.nodes if node not in visitados}
        atual = min(nao_visitados, key=nao_visitados.get)
        visitados.add(atual)
        
        for vizinho in grafo.neighbors(atual):
            peso = grafo[atual][vizinho]['weight']
            if dist[atual] + peso < dist[vizinho]:
                dist[vizinho] = dist[atual] + peso
                ant[vizinho] = atual
    return dist, ant

def reconstruir_rota(ant, inicio, destino):
    caminho = []
    atual = destino
    while atual != inicio:
        if atual is None:
            return []  # Sem rota
        caminho.append(atual)
        atual = ant[atual]
    caminho.append(inicio)
    caminho.reverse()
    return caminho

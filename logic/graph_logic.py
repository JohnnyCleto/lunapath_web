import networkx as nx
import random

LOCAIS = [
    "Casa de Luna", "Estação de Drones", "Auditoria Principal", "Estação IoT", "Cafeteria Tech",
    "Central de Energia", "Hospital Futuro", "Escola Smart", "Museu Digital", "Estúdio Holográfico",
    "Praça do Conhecimento", "Biblioteca AR", "Centro de Robótica", "Galeria Virtual", "Laboratório Quântico",
    "Centro de Inovação", "Mercado Automatizado", "Estação Solar", "Zoológico Digital", "Residência Cyborg",
    "Teatro de Realidade Mista", "Parque Inteligente", "Clínica de Nanomedicina", "Delegacia Neural",
    "Terminal de Ônibus Autônomo", "Garagem de Veículos AI", "Torre de Comunicação 5G", "Observatório de Dados",
    "Laboratório Genético", "Academia VR", "Centro Financeiro Blockchain", "Cinema Imersivo",
    "Ponto de Recarga Elétrica", "Estufa Inteligente", "Fábrica Automatizada", "Base de Drones",
    "Túnel Subterrâneo A", "Túnel Subterrâneo B", "Ponto de Encontro AR", "Posto de Vigilância",
    "Jardim Algorítmico", "Escola Infantil Digital", "Restaurante Autônomo", "Campus AI", "Condomínio Verde",
    "Vila Modular", "Câmara de Simulação", "Núcleo de Energia Limpa", "Rooftop Garden", "Estação Suborbital"
]

def gerar_mapa_cidade():
    random.seed()  # Pode fixar um valor para teste, ex: random.seed(42)

    cidade = nx.Graph()
    posicoes = {}

    # Adiciona nós com posições aleatórias
    for nome in LOCAIS:
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        cidade.add_node(nome, pos=(x, y))

    # Para garantir que o grafo seja conexo, cria uma "árvore geradora mínima" simples:
    locais_restantes = LOCAIS[:]
    locais_conectados = [locais_restantes.pop(0)]  # Começa com o primeiro local

    while locais_restantes:
        origem = random.choice(locais_conectados)
        destino = locais_restantes.pop(0)
        peso = random.randint(1, 10)
        cidade.add_edge(origem, destino, weight=peso)
        locais_conectados.append(destino)

    # Agora adiciona arestas aleatórias extras para criar conexões
    chance_conexao = 0.3  # 30% de chance de criar uma conexão extra entre pares
    n = len(LOCAIS)
    for i in range(n):
        for j in range(i + 1, n):
            if not cidade.has_edge(LOCAIS[i], LOCAIS[j]) and random.random() < chance_conexao:
                peso = random.randint(1, 10)
                cidade.add_edge(LOCAIS[i], LOCAIS[j], weight=peso)

    return cidade

def dijkstra(grafo, origem):
    dist = {node: float('inf') for node in grafo.nodes}
    dist[origem] = 0
    ant = {node: None for node in grafo.nodes}
    visitados = set()

    while len(visitados) < len(grafo.nodes):
        atual = min((n for n in grafo.nodes if n not in visitados), key=lambda n: dist[n])
        visitados.add(atual)

        for vizinho in grafo.neighbors(atual):
            peso = grafo[atual][vizinho]["weight"]
            if dist[atual] + peso < dist[vizinho]:
                dist[vizinho] = dist[atual] + peso
                ant[vizinho] = atual

    return dist, ant

def reconstruir_rota(anteriores, origem, destino):
    rota = []
    atual = destino
    while atual != origem:
        anterior = anteriores[atual]
        if anterior is None:
            return []
        rota.append((anterior, atual))
        atual = anterior
    rota.reverse()
    return rota

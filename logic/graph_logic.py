import networkx as nx
import random

# Lista de 50 locais nomeados de uma cidade inteligente fictícia
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

# Conexões manuais (nome do local 1, nome do local 2, peso)
CONEXOES = [
    ("Casa de Luna", "Estação de Drones", 4),
    ("Casa de Luna", "Parque Inteligente", 3),
    ("Casa de Luna", "Delegacia Neural", 5),
    ("Estação de Drones", "Auditoria Principal", 3),
    ("Estação de Drones", "Cafeteria Tech", 2),
    ("Estação IoT", "Casa de Luna", 6),
    ("Estação IoT", "Escola Smart", 3),
    ("Cafeteria Tech", "Base de Drones", 2),
    ("Base de Drones", "Clínica de Nanomedicina", 2),
    ("Clínica de Nanomedicina", "Hospital Futuro", 3),
    ("Hospital Futuro", "Posto de Vigilância", 2),
    ("Posto de Vigilância", "Centro de Inovação", 1),
    ("Centro de Inovação", "Residência Cyborg", 2),
    ("Residência Cyborg", "Teatro de Realidade Mista", 2),
    ("Teatro de Realidade Mista", "Trilha Sensorial", 1),
    ("Trilha Sensorial", "Campus AI", 1),
    ("Campus AI", "Observatório de Dados", 2),
    ("Observatório de Dados", "Estufa Inteligente", 2),
    ("Estufa Inteligente", "Fábrica Automatizada", 1),
    ("Fábrica Automatizada", "Centro de Robótica", 2),
    ("Centro de Robótica", "Museu Digital", 2),
    ("Museu Digital", "Centro Financeiro Blockchain", 2),
    ("Centro Financeiro Blockchain", "Escola Infantil Digital", 1),
    ("Escola Infantil Digital", "Escola Smart", 1),
    ("Escola Smart", "Garagem de Veículos AI", 2),
    ("Garagem de Veículos AI", "Laboratório Genético", 1),
    ("Laboratório Genético", "Auditoria Principal", 2),
    ("Laboratório Genético", "Cafeteria Tech", 1),
    ("Cafeteria Tech", "Vila Modular", 1),
    ("Vila Modular", "Clínica de Nanomedicina", 2),
    ("Auditoria Principal", "Estação Solar", 2),
    ("Estação Solar", "Núcleo de Energia Limpa", 2),
    ("Núcleo de Energia Limpa", "Academia VR", 2),
    ("Academia VR", "Estação Suborbital", 2),
    ("Estação Suborbital", "Zoológico Digital", 1),
    ("Zoológico Digital", "Posto de Vigilância", 1),
    ("Museu Digital", "Praça do Conhecimento", 2),
    ("Praça do Conhecimento", "Biblioteca AR", 1),
    ("Biblioteca AR", "Torre de Comunicação 5G", 1),
    ("Torre de Comunicação 5G", "Centro Financeiro Blockchain", 1),
    ("Garagem de Veículos AI", "Ponto de Encontro AR", 2),
    ("Delegacia Neural", "Ponto de Encontro AR", 1),
    ("Túnel Subterrâneo A", "Hospital Futuro", 1),
    ("Túnel Subterrâneo A", "Laboratório Quântico", 2),
    ("Laboratório Quântico", "Cinema Imersivo", 1),
    ("Cinema Imersivo", "Academia VR", 2),
    ("Túnel Subterrâneo B", "Estação IoT", 2),
    ("Túnel Subterrâneo B", "Praça do Conhecimento", 1),
    ("Rooftop Garden", "Clínica de Nanomedicina", 2),
]

def gerar_mapa_cidade():
    cidade = nx.Graph()
    posicoes = {}

    for nome in LOCAIS:
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        posicoes[nome] = (x, y)
        cidade.add_node(nome, pos=(x, y))

    for origem, destino, peso in CONEXOES:
        if origem in cidade.nodes and destino in cidade.nodes:
            cidade.add_edge(origem, destino, weight=peso)

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

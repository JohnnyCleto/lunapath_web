import networkx as nx
from math import sqrt
import heapq
import random  # <-- Corrigido

# Definição dos locais com coordenadas
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

def gerar_mapa_cidade():
    G = nx.Graph()
    for local, pos in LOCAIS.items():
        G.add_node(local, pos=pos)

    conexoes = [
        ("Casa de Luna", "Delegacia Neural"), ("Casa de Luna", "Parque Inteligente"),
        ("Delegacia Neural", "Estação de Drones"), ("Delegacia Neural", "Garagem de Veículos AI"),
        ("Parque Inteligente", "Estação IoT"), ("Parque Inteligente", "Praça do Conhecimento"),
        ("Estação de Drones", "Garagem de Veículos AI"), ("Garagem de Veículos AI", "Auditoria Principal"),
        ("Auditoria Principal", "Cafeteria Tech"), ("Auditoria Principal", "Estação Solar"),
        ("Cafeteria Tech", "Hospital Futuro"), ("Hospital Futuro", "Zoológico Digital"),
        ("Hospital Futuro", "Central de Energia"), ("Estação IoT", "Escola Smart"),
        ("Escola Smart", "Museu Digital"), ("Museu Digital", "Galeria Virtual"),
        ("Galeria Virtual", "Residência Cyborg"), ("Residência Cyborg", "Teatro de Realidade Mista"),
        ("Teatro de Realidade Mista", "Estufa Inteligente"), ("Estufa Inteligente", "Fábrica Automatizada"),
        ("Fábrica Automatizada", "Centro de Robótica"), ("Centro de Robótica", "Biblioteca AR"),
        ("Biblioteca AR", "Praça do Conhecimento"), ("Praça do Conhecimento", "Centro Financeiro Blockchain"),
        ("Centro Financeiro Blockchain", "Ponto de Recarga Elétrica"), ("Ponto de Recarga Elétrica", "Estação Solar"),
        ("Estação Solar", "Laboratório Quântico"), ("Laboratório Quântico", "Centro de Inovação"),
        ("Centro de Inovação", "Clínica de Nanomedicina"), ("Clínica de Nanomedicina", "Central de Energia"),
        ("Central de Energia", "Terminal de Ônibus Autônomo"), ("Terminal de Ônibus Autônomo", "Museu Digital"),
        ("Terminal de Ônibus Autônomo", "Escola Smart"), ("Terminal de Ônibus Autônomo", "Garagem de Veículos AI"),
        ("Torre de Comunicação 5G", "Biblioteca AR"), ("Torre de Comunicação 5G", "Praça do Conhecimento"),
        ("Núcleo de IA", "Academia VR"), ("Academia VR", "Cinema Imersivo"),
        ("Cinema Imersivo", "Estação Solar"), ("Núcleo de IA", "Centro de Transporte Magnético"),
        ("Centro de Transporte Magnético", "Plataforma de Lançamento Espacial"),
        ("Plataforma de Lançamento Espacial", "Teatro de Realidade Mista"),
        ("Centro de Transporte Magnético", "Observatório de Dados"), ("Observatório de Dados", "Galeria Virtual"),
        ("Observatório de Dados", "Fábrica Automatizada"), ("Laboratório Genético", "Auditoria Principal"),
        ("Laboratório Genético", "Núcleo de IA"), ("Ponte Holográfica", "Centro de Transporte Magnético"),
        ("Ponte Holográfica", "Plataforma de Lançamento Espacial"),
        ("Túnel Subterrâneo A", "Laboratório Quântico"), ("Túnel Subterrâneo A", "Laboratório Genético"),
        ("Túnel Subterrâneo B", "Central de Energia"), ("Túnel Subterrâneo B", "Clínica de Nanomedicina"),
        ("Base de Drones", "Estação IoT"), ("Base de Drones", "Hospital Futuro"),
        ("Estação de Reciclagem Avançada", "Estufa Inteligente"), ("Parque Eólico Inteligente", "Estação de Reciclagem Avançada"),
        ("Parque Eólico Inteligente", "Plataforma de Lançamento Espacial"),
    ]

    for u, v in conexoes:
        pos_u, pos_v = G.nodes[u]["pos"], G.nodes[v]["pos"]
        peso = sqrt((pos_u[0] - pos_v[0])**2 + (pos_u[1] - pos_v[1])**2)
        G.add_edge(u, v, weight=peso)
    return G

def atualizar_pesos_iot(grafo, sensores):
    fator = 10
    for u, v in grafo.edges():
        chave = (u, v)
        congestao = sensores.get(chave, 0)
        pos_u, pos_v = grafo.nodes[u]["pos"], grafo.nodes[v]["pos"]
        peso_original = sqrt((pos_u[0] - pos_v[0])**2 + (pos_u[1] - pos_v[1])**2)
        grafo[u][v]["weight"] = peso_original * (1 + fator * congestao)

def dijkstra_dinamico(grafo, origem, prioridade="tempo"):
    dist = {n: float("inf") for n in grafo.nodes}
    dist[origem] = 0
    ant = {}
    heap = [(0, origem)]

    while heap:
        d, u = heapq.heappop(heap)
        for v in grafo.neighbors(u):
            peso = grafo[u][v]['weight']
            if dist[v] > d + peso:
                dist[v] = d + peso
                ant[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, ant

def reconstruir_rota(ant, origem, destino):
    rota = []
    atual = destino
    while atual != origem:
        rota.append(atual)
        atual = ant.get(atual)
        if atual is None:
            return []
    rota.append(origem)
    rota.reverse()
    return rota

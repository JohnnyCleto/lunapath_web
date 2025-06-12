import networkx as nx
import random
import heapq
from math import sqrt

LOCAIS = {
    "Casa de Luna": (10, 10, "Residência"),
    "Estação de Drones": (40, 20, "Transporte"),
    "Auditoria Principal": (70, 10, "Empresa"),
    "Estação IoT": (20, 50, "Tecnologia"),
    "Cafeteria Tech": (60, 40, "Alimentação"),
    "Central de Energia": (80, 20, "Energia"),
    "Hospital Futuro": (90, 60, "Hospital"),
    "Escola Smart": (40, 90, "Educação"),
    "Museu Digital": (60, 110, "Cultura"),
    "Estúdio Holográfico": (80, 110, "Mídia"),
    "Praça do Conhecimento": (10, 110, "Lazer"),
    "Biblioteca AR": (20, 130, "Cultura"),
    "Centro de Robótica": (70, 130, "Tecnologia"),
    "Galeria Virtual": (90, 130, "Cultura"),
    "Laboratório Quântico": (100, 40, "Pesquisa"),
    "Centro de Inovação": (100, 80, "Empresa"),
    "Mercado Automatizado": (60, 150, "Comércio"),
    "Estação Solar": (90, 10, "Energia"),
    "Zoológico Digital": (110, 60, "Lazer"),
    "Residência Cyborg": (100, 130, "Residência"),
    "Teatro de Realidade Mista": (110, 150, "Lazer"),
    "Parque Inteligente": (10, 30, "Lazer"),
    "Clínica de Nanomedicina": (80, 70, "Hospital"),
    "Delegacia Neural": (20, 20, "Segurança"),
    "Terminal de Ônibus Autônomo": (70, 90, "Transporte"),
    "Garagem de Veículos AI": (40, 40, "Transporte"),
    "Torre de Comunicação 5G": (10, 130, "Tecnologia"),
    "Observatório de Dados": (90, 150, "Pesquisa"),
    "Laboratório Genético": (60, 20, "Pesquisa"),
    "Academia VR": (110, 20, "Educação"),
    "Centro Financeiro Blockchain": (20, 110, "Empresa"),
    "Cinema Imersivo": (100, 10, "Lazer"),
    "Ponto de Recarga Elétrica": (40, 130, "Energia"),
    "Estufa Inteligente": (70, 150, "Pesquisa"),
    "Fábrica Automatizada": (80, 130, "Empresa"),
    "Base de Drones": (60, 60, "Tecnologia"),
    "Túnel Subterrâneo A": (90, 40, "Infraestrutura"),
    "Túnel Subterrâneo B": (100, 70, "Infraestrutura"),
    "Ponte Holográfica": (110, 90, "Infraestrutura"),
    "Plataforma de Lançamento Espacial": (130, 110, "Tecnologia"),
    "Núcleo de IA": (130, 20, "Tecnologia"),
    "Centro de Transporte Magnético": (120, 60, "Transporte"),
    "Estação de Reciclagem Avançada": (130, 40, "Energia"),
    "Parque Eólico Inteligente": (140, 80, "Energia"),
}

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

def criar_grafo():
    G = nx.Graph()
    for local, (x, y, tipo) in LOCAIS.items():
        G.add_node(local, pos=(x, y), tipo=tipo)
    for u, v in CONEXOES:
        dist = distancia_euclidiana(LOCAIS[u][:2], LOCAIS[v][:2])
        G.add_edge(u, v, weight=dist, blocked=False, congestion=1.0)
    return G

def dijkstra(grafo, inicio, fim, modo="curto"):
    dist = {n: float("inf") for n in grafo.nodes}
    prev = {n: None for n in grafo.nodes}
    dist[inicio] = 0
    heap = [(0, inicio)]
    while heap:
        d_u, u = heapq.heappop(heap)
        if u == fim:
            break
        if d_u > dist[u]:
            continue
        for v in grafo.neighbors(u):
            ed = grafo[u][v]
            if ed["blocked"]:
                continue
            peso = ed["weight"]
            if modo == "seguro" and ed["congestion"] > 1.5:
                peso *= 1.5
            if modo == "turistico" and grafo.nodes[v]["tipo"] in ("Cultura", "Lazer"):
                peso *= 0.7
            nd = d_u + peso
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    path = []
    node = fim
    while node:
        path.insert(0, node)
        node = prev[node]
    return path, dist[fim]

def calcular_caminho(grafo, origem, destino, modo="curto"):
    return dijkstra(grafo, origem, destino, modo)

def calcular_custo_caminho(grafo, caminho):
    custo = 0.0
    for i in range(len(caminho)-1):
        ed = grafo[caminho[i]][caminho[i+1]]
        custo += ed["weight"] * ed.get("congestion", 1.0)
    return custo

def atualizar_eventos(grafo):
    eventos = []
    for u, v in grafo.edges:
        if random.random() < 0.1:
            grafo[u][v]["blocked"] = True
            eventos.append(f"🚧 Bloqueio entre {u} e {v}")
        else:
            grafo[u][v]["blocked"] = False
        if random.random() < 0.2:
            cong = round(random.uniform(1.0, 3.0), 2)
            grafo[u][v]["congestion"] = cong
            if cong > 2.0:
                eventos.append(f"🚦 Congestionamento severo entre {u} e {v} (x{cong})")
        else:
            grafo[u][v]["congestion"] = 1.0
    if not eventos:
        eventos.append("🎉 Todas as rotas estão livres!")
    return eventos
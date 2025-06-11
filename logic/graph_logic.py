import networkx as nx
from math import sqrt
import random
import heapq


# Localizações definidas com espaçamento adequado para visualização clara e realista
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
    "Plataforma de Lançamento": (10, 70),
    "Parque Eólico": (20, 90),
    "Porto Autônomo": (40, 110),
    "Terminal de Carga AI": (70, 110),
    "Central de Monitoramento": (90, 110),
    "Estação de Reciclagem": (100, 150),
    "Parque de Energia": (110, 130),
    "Centro Médico Neural": (20, 40),
    "Cemitério Digital": (40, 150),
}

CONEXOES = [
    ("Casa de Luna", "Parque Inteligente"),
    ("Casa de Luna", "Delegacia Neural"),
    ("Parque Inteligente", "Estação IoT"),
    ("Delegacia Neural", "Estação de Drones"),
    ("Estação de Drones", "Garagem de Veículos AI"),
    ("Garagem de Veículos AI", "Auditoria Principal"),
    ("Auditoria Principal", "Central de Energia"),
    ("Central de Energia", "Laboratório Quântico"),
    ("Laboratório Quântico", "Túnel Subterrâneo A"),
    ("Túnel Subterrâneo A", "Túnel Subterrâneo B"),
    ("Túnel Subterrâneo B", "Centro de Inovação"),
    ("Centro de Inovação", "Residência Cyborg"),
    ("Residência Cyborg", "Teatro de Realidade Mista"),
    ("Teatro de Realidade Mista", "Galeria Virtual"),
    ("Galeria Virtual", "Estúdio Holográfico"),
    ("Estúdio Holográfico", "Museu Digital"),
    ("Museu Digital", "Biblioteca AR"),
    ("Biblioteca AR", "Torre de Comunicação 5G"),
    ("Torre de Comunicação 5G", "Praça do Conhecimento"),
    ("Praça do Conhecimento", "Centro Financeiro Blockchain"),
    ("Centro Financeiro Blockchain", "Escola Smart"),
    ("Escola Smart", "Terminal de Ônibus Autônomo"),
    ("Terminal de Ônibus Autônomo", "Cafeteria Tech"),
    ("Cafeteria Tech", "Base de Drones"),
    ("Base de Drones", "Hospital Futuro"),
    ("Hospital Futuro", "Clínica de Nanomedicina"),
    ("Clínica de Nanomedicina", "Central de Monitoramento"),
    ("Central de Monitoramento", "Laboratório Genético"),
    ("Laboratório Genético", "Mercado Automatizado"),
    ("Mercado Automatizado", "Estufa Inteligente"),
    ("Estufa Inteligente", "Fábrica Automatizada"),
    ("Fábrica Automatizada", "Parque de Energia"),
    ("Parque de Energia", "Parque Eólico"),
    ("Parque Eólico", "Terminal de Carga AI"),
    ("Terminal de Carga AI", "Porto Autônomo"),
    ("Porto Autônomo", "Ponto de Recarga Elétrica"),
    ("Ponto de Recarga Elétrica", "Cinema Imersivo"),
    ("Cinema Imersivo", "Academia VR"),
    ("Academia VR", "Estação Solar"),
    ("Estação Solar", "Observatório de Dados"),
    ("Observatório de Dados", "Cemitério Digital"),
    ("Cemitério Digital", "Parque Inteligente"),
    ("Parque Inteligente", "Centro Médico Neural"),
    ("Centro Médico Neural", "Delegacia Neural"),
]


def distancia(p1, p2):
    """Calcula distância Euclidiana entre dois pontos."""
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def gerar_mapa_cidade():
    """Cria grafo com nós, posições e conexões, adicionando pesos baseados na distância."""
    G = nx.DiGraph()
    for local, pos in LOCAIS.items():
        G.add_node(local, pos=pos)
    for origem, destino in CONEXOES:
        dist = distancia(LOCAIS[origem], LOCAIS[destino])
        G.add_edge(origem, destino, weight=dist)
        G.add_edge(destino, origem, weight=dist)
    return G


def atualizar_pesos_iot(grafo, sensores_iot):
    """
    Atualiza pesos das arestas do grafo baseando-se no congestionamento informado pelos sensores IoT.
    peso_real = peso_base * (1 + fator_congestionamento)
    """
    for u, v, data in grafo.edges(data=True):
        congestionamento = sensores_iot.get((u, v), 0)
        base = distancia(grafo.nodes[u]["pos"], grafo.nodes[v]["pos"])
        data["weight"] = base * (1 + congestionamento)


def dijkstra_dinamico(grafo, origem, prioridade="tempo"):
    """
    Algoritmo de Dijkstra com prioridade:
    - "tempo": minimiza peso normal.
    - "evitar_congestionamento": penaliza arestas com peso alto.
    
    Retorna: dist, ant
    """
    dist = {node: float("inf") for node in grafo.nodes}
    ant = {node: None for node in grafo.nodes}
    dist[origem] = 0
    fila = [(0, origem)]

    while fila:
        custo_atual, u = heapq.heappop(fila)
        if custo_atual > dist[u]:
            continue

        for v in grafo.neighbors(u):
            peso = grafo[u][v]["weight"]

            if prioridade == "evitar_congestionamento":
                penalidade = max(0, peso - distancia(grafo.nodes[u]["pos"], grafo.nodes[v]["pos"]))
                peso += penalidade * 2

            if dist[u] + peso < dist[v]:
                dist[v] = dist[u] + peso
                ant[v] = u
                heapq.heappush(fila, (dist[v], v))

    return dist, ant


def reconstruir_rota(antecessores, origem, destino):
    """Reconstrói rota do destino até origem usando dicionário de antecessores."""
    rota = []
    atual = destino
    while atual is not None:
        rota.append(atual)
        if atual == origem:
            break
        atual = antecessores[atual]
    rota.reverse()
    if rota[0] != origem:
        return []  # rota inválida
    return rota


def simular_situacoes_imprevistas(grafo, origem, destino):
    """
    Simula situações imprevistas que podem alterar o cálculo da rota:
    - Pode bloquear uma aresta.
    - Pode aumentar o congestionamento temporário em certas conexões.
    - Pode gerar uma rota alternativa aleatória se bloqueios ocorrem.
    
    Retorna: rota, info (detalhes da rota e situação)
    """
    # Copia o grafo para manipular sem alterar original
    G_sim = grafo.copy()

    # Simular evento aleatório: com 30% de chance, bloqueia uma aresta aleatória
    if random.random() < 0.3:
        arestas = list(G_sim.edges())
        bloqueio = random.choice(arestas)
        u, v = bloqueio
        G_sim.remove_edge(u, v)
        # info do evento
        evento = f"Aresta bloqueada temporariamente entre '{u}' e '{v}'."
    else:
        evento = "Nenhum bloqueio detectado."

    # Simular congestionamento variável
    sensores_iot = {}
    for u, v in G_sim.edges():
        # congestionamento entre 0 e 0.5 randomicamente
        sensores_iot[(u, v)] = random.uniform(0, 0.5)
    atualizar_pesos_iot(G_sim, sensores_iot)

    # Calcular rota considerando congestionamento e possíveis bloqueios
    dist, ant = dijkstra_dinamico(G_sim, origem, prioridade="evitar_congestionamento")
    rota = reconstruir_rota(ant, origem, destino)

    if not rota:
        return [], f"Não foi possível encontrar rota entre '{origem}' e '{destino}' devido a bloqueios."

    # Calcular distância total da rota
    distancia_total = sum(
        distancia(G_sim.nodes[rota[i]]["pos"], G_sim.nodes[rota[i + 1]]["pos"])
        for i in range(len(rota) - 1)
    )

    # Estimar tempo considerando congestionamento médio da rota
    pesos_rota = [
        G_sim[rota[i]][rota[i + 1]]["weight"]
        for i in range(len(rota) - 1)
    ]
    tempo_estimado = sum(pesos_rota)  # tempo em unidades relativas

    info_rota = (
        f"Rota calculada entre '{origem}' e '{destino}':\n"
        f"  - Número de pontos: {len(rota)}\n"
        f"  - Distância total (Euclidiana): {distancia_total:.2f} unidades\n"
        f"  - Tempo estimado considerando congestionamento: {tempo_estimado:.2f} unidades\n"
        f"  - Evento imprevisto: {evento}\n"
        f"  - Caminho: {' -> '.join(rota)}"
    )

    return rota, info_rota


# EXEMPLO DE USO
if __name__ == "__main__":
    mapa = gerar_mapa_cidade()
    origem = "Casa de Luna"
    destino = "Teatro de Realidade Mista"

    rota, info = simular_situacoes_imprevistas(mapa, origem, destino)
    print(info)
